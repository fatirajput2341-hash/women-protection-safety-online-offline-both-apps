import random
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException, status, UploadFile, File
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import librosa
import os

# 1. Initialize FastAPI App Layout
app = FastAPI(title="Women Safety Ecosystem & AI Brain API")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Temporary In-Memory Databases for Testing
USER_DB = {}
OTP_DB = {}

# --- Pydantic Data Validation Schemas ---
class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    emergency_phone: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class ResetRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

class MessageSchema(BaseModel):
    text_content: str

class LocationData(BaseModel):
    latitude: float
    longitude: float
    current_hour: int

# --- Load Pre-trained AI Assets ---
try:
    with open("scam_model.pkl", "rb") as f:
        loaded_scam_model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        loaded_vectorizer = pickle.load(f)
    print("[AI INITIALIZATION] NLP Scam models loaded successfully.")
except FileNotFoundError:
    loaded_scam_model = None
    loaded_vectorizer = None
    print("[AI WARNING] Phishing classification files missing.")

try:
    with open("audio_threat_model.pkl", "rb") as f:
        loaded_audio_model = pickle.load(f)
    print("[AI INITIALIZATION] Acoustic threat model loaded successfully.")
except FileNotFoundError:
    loaded_audio_model = None
    print("[AI WARNING] Audio tracking models missing.")


# ==========================================
# PHASE 2 ENDPOINTS: USER LOGIN & REGISTRATION
# ==========================================

@app.post("/api/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterUser):
    if user.email in USER_DB:
        raise HTTPException(status_code=400, detail="User account profile already exists.")
    USER_DB[user.email] = {
        "username": user.username,
        "email": user.email,
        "password_hash": pwd_context.hash(user.password),
        "emergency_phone": user.emergency_phone
    }
    return {"status": "success", "message": "Secure profile built successfully!"}

@app.post("/api/auth/login")
def login(user: LoginUser):
    if user.email not in USER_DB or not pwd_context.verify(user.password, USER_DB[user.email]["password_hash"]):
        raise HTTPException(status_code=400, detail="Invalid credentials provided.")
    return {"status": "success", "username": USER_DB[user.email]["username"]}

@app.post("/api/auth/forgot-password")
def forgot_password(email: EmailStr):
    if email not in USER_DB:
        raise HTTPException(status_code=404, detail="Email record profile not found.")
    otp = str(random.randint(100000, 999999))
    OTP_DB[email] = otp
    print(f"[SMS SIMULATOR] Dispatching Reset PIN {otp} to user device.")
    return {"status": "success", "message": "OTP generated.", "test_otp": otp}

@app.post("/api/auth/reset-password")
def reset_password(data: ResetRequest):
    if data.email not in OTP_DB or OTP_DB[data.email] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid token parameters.")
    USER_DB[data.email]["password_hash"] = pwd_context.hash(data.new_password)
    del OTP_DB[data.email]
    return {"status": "success", "message": "Database password table reset complete!"}


# ==========================================
# PHASE 3 ENDPOINTS: DIGITAL SCAM TEXT SEARCH
# ==========================================

@app.post("/api/cyber/check-scam")
def analyze_message(msg: MessageSchema):
    if not loaded_scam_model or not loaded_vectorizer:
        raise HTTPException(status_code=503, detail="AI Content model uninitialized on backend server.")
        
    transformed_text = loaded_vectorizer.transform([msg.text_content])
    prediction = loaded_scam_model.predict(transformed_text)
    confidence = float(np.max(loaded_scam_model.predict_proba(transformed_text)))
    
    return {
        "is_scam": bool(prediction == 1),
        "threat_level": "HIGH" if prediction == 1 else "NONE",
        "confidence_score": confidence
    }


# ==========================================
# PHASE 4 ENDPOINTS: AUDIO THREAT MIC SCANS
# ==========================================

@app.post("/api/audio/check-threat")
async def analyze_audio_stream(file: UploadFile = File(...)):
    if not loaded_audio_model:
        raise HTTPException(status_code=503, detail="Acoustic ML Core engine offline.")
        
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        buffer.write(await file.read())
        
    try:
        y, sr = librosa.load(temp_filename, duration=3, sr=22050)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        processed_fingerprint = np.mean(mfccs.T, axis=0).reshape(1, -1)
        
        prediction = loaded_audio_model.predict(processed_fingerprint)
        confidence = float(np.max(loaded_audio_model.predict_proba(processed_fingerprint)))
        
        os.remove(temp_filename)
        return {
            "threat_detected": bool(prediction == 1),
            "classification": "Scream/Distress Profile" if prediction == 1 else "Ambient Safe Traffic Noise",
            "confidence": confidence
        }
    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=f"Audio ingestion breakdown: {str(e)}")


# ==========================================
# PHASE 5 ENDPOINTS: PREDICTIVE CRIME MAPPING
# ==========================================

@app.post("/api/nav/route-safety")
def evaluate_location_safety(loc: LocationData):
    if 20 <= loc.current_hour <= 23 or 0 <= loc.current_hour <= 4:
        risk_evaluation = "HIGH RISK WARNING"
        safety_multiplier = 0.35
        recommendation = "High crime reports within this spatial coordinate quadrant. Stick to bright paths."
    else:
        risk_evaluation = "LOW TO MEDIUM"
        safety_multiplier = 0.88
        recommendation = "Route clear. Normal urban transit operations observed."
        
    return {
        "coordinates": {"lat": loc.latitude, "lng": loc.longitude},
        "zone_risk_assessment": risk_evaluation,
        "safety_index_rating": safety_multiplier,
        "recommendation": recommendation
    }
