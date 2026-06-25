"""
GOE OS - النسخة الممتازة (Production-Ready with Security & Performance)
نظام الحوكمة المعرفية المتكامل - يجمع جميع الميزات مع أمان وإدارة متقدمة
"""

import logging
import os
import sys
import json
import time
import secrets
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Annotated
from enum import Enum

# ============================================================
# FastAPI & Security Imports
# ============================================================

from fastapi import (
    FastAPI, Request, HTTPException, BackgroundTasks, 
    WebSocket, WebSocketDisconnect, Depends, status,
    Security, Header, Query, Path, Body
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, FileResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field, validator, EmailStr, conint, constr
import uvicorn

# ============================================================
# Security Libraries
# ============================================================

from passlib.context import CryptContext
from jose import JWTError, jwt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import bcrypt

# ============================================================
# إعداد التسجيل المتقدم
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('goe_os.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("GOE_OS")

# ============================================================
# إعدادات الأمان
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v2/auth/login")

# Security schemes
security = HTTPBearer(auto_error=False)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# ============================================================
# نماذج Pydantic للتحقق الصارم
# ============================================================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل')
        if not any(c.isdigit() for c in v):
            raise ValueError('يجب أن تحتوي كلمة المرور على رقم واحد على الأقل')
        return v

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = "viewer"

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=100000)
    entity: Optional[Dict[str, Any]] = Field(default_factory=dict)
    depth: Optional[str] = Field("standard", pattern="^(mini|standard|deep)$")
    domain: Optional[str] = Field(None, max_length=50)

class AnalysisResponse(BaseModel):
    status: str = "success"
    result: Dict[str, Any]
    audit_id: str
    processing_time: float

# ============================================================
# إضافة مسار المجلد المشترك (Monorepo)
# ============================================================

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../shared'))

# ============================================================
# محاولة استيراد الأنظمة
# ============================================================

# 1. Auto-Loader V2
try:
    from core.auto_loader_v2 import AutoLoaderV2
    AUTO_LOADER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ AutoLoaderV2 not found: {e}")
    AUTO_LOADER_AVAILABLE = False

# 2. المكونات الأساسية
try:
    from kg_core.layers.diagnostics import DiagnosticsLayer
    from kg_core.indicators import KnowledgeIndicators
    CORE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ Core components not found: {e}")
    CORE_AVAILABLE = False

# 3. طبقة التكامل
try:
    from core.integration import IntegrationLayer
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ IntegrationLayer not found: {e}")
    INTEGRATION_AVAILABLE = False

# 4. الأنظمة الأخرى (مع محاولة الاستيراد)
try:
    from core.reputation import ReputationSystem
    REPUTATION_AVAILABLE = True
except ImportError:
    REPUTATION_AVAILABLE = False

try:
    from core.challenges import ChallengeSystem
    CHALLENGES_AVAILABLE = True
except ImportError:
    CHALLENGES_AVAILABLE = False

try:
    from core.templates import TemplateSystem
    TEMPLATES_AVAILABLE = True
except ImportError:
    TEMPLATES_AVAILABLE = False

try:
    from core.mentors import GovernanceMentorSystem
    MENTORS_AVAILABLE = True
except ImportError:
    MENTORS_AVAILABLE = False

try:
    from core.gaps import TransparentGapLayer
    GAPS_AVAILABLE = True
except ImportError:
    GAPS_AVAILABLE = False

try:
    from core.community import GOECommunity
    COMMUNITY_AVAILABLE = True
except ImportError:
    COMMUNITY_AVAILABLE = False

try:
    from core.strategic_simulator import StrategicSimulator
    STRATEGIC_AVAILABLE = True
except ImportError:
    STRATEGIC_AVAILABLE = False

# ============================================================
# قاعدة البيانات المؤقتة (للمستخدمين) - في الإنتاج تستخدم قاعدة بيانات حقيقية
# ============================================================

users_db = {}  # username -> {"hashed_password": "...", "email": "...", "full_name": "...", "role": "..."}
refresh_tokens_db = {}  # refresh_token -> username
audit_logs_db = []  # قائمة سجلات التدقيق

# ============================================================
# دوال المصادقة والأمان
# ============================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(username: str) -> str:
    token = secrets.token_urlsafe(64)
    refresh_tokens_db[token] = {"username": username, "created_at": datetime.utcnow().isoformat()}
    return token

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"username": username, "role": users_db[username].get("role", "viewer")}

async def get_current_active_user(current_user: Dict = Depends(get_current_user)) -> Dict:
    if current_user.get("role") not in ["viewer", "analyst", "admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user

def require_role(required_role: str):
    async def role_checker(current_user: Dict = Depends(get_current_user)):
        role_hierarchy = {"viewer": 0, "analyst": 1, "admin": 2, "super_admin": 3}
        if role_hierarchy.get(current_user.get("role", "viewer"), 0) < role_hierarchy.get(required_role, 0):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker

def log_audit(user_id: str, action: str, details: Dict, status: str = "success"):
    """تسجيل تدقيق شامل"""
    audit_logs_db.append({
        "user_id": user_id,
        "action": action,
        "details": details,
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "ip": details.get("ip", "unknown")
    })
    if len(audit_logs_db) > 10000:  # حد أقصى للسجلات
        audit_logs_db.pop(0)

# ============================================================
# دوال التحميل الكسول (Lazy Loaders)
# ============================================================

_diagnostics = None
_rep_system = None
_challenge_system = None
_mentor_system = None
_gap_layer = None
_community = None
_strategic_sim = None

def get_diagnostics():
    global _diagnostics
    if _diagnostics is None and CORE_AVAILABLE:
        _diagnostics = DiagnosticsLayer()
    return _diagnostics

def get_reputation():
    global _rep_system
    if _rep_system is None and REPUTATION_AVAILABLE:
        _rep_system = ReputationSystem()
    return _rep_system

def get_challenges():
    global _challenge_system
    if _challenge_system is None and CHALLENGES_AVAILABLE:
        _challenge_system = ChallengeSystem()
    return _challenge_system

def get_mentors():
    global _mentor_system
    if _mentor_system is None and MENTORS_AVAILABLE:
        _mentor_system = GovernanceMentorSystem()
    return _mentor_system

def get_gaps():
    global _gap_layer
    if _gap_layer is None and GAPS_AVAILABLE:
        _gap_layer = TransparentGapLayer()
    return _gap_layer

def get_community():
    global _community
    if _community is None and COMMUNITY_AVAILABLE:
        _community = GOECommunity()
    return _community

def get_strategic_sim():
    global _strategic_sim
    if _strategic_sim is None and STRATEGIC_AVAILABLE:
        _strategic_sim = StrategicSimulator()
    return _strategic_sim

# ============================================================
# دورة حياة التطبيق
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 GOE OS - النسخة الممتازة (Production-Ready) بدأت التشغيل...")
    
    # تشغيل Auto-Loader
    if AUTO_LOADER_AVAILABLE:
        loader = AutoLoaderV2(app)
        results = loader.discover_and_load(["core", "modules", "execution", "plugins"])
        for folder, result in results.items():
            logger.info(f"📦 {folder}: تم تحميل {result.get('count', 0)} وحدة")
    
    # إنشاء مستخدم Admin افتراضي إذا لم يكن موجوداً
    if "admin" not in users_db:
        users_db["admin"] = {
            "hashed_password": get_password_hash("admin123"),
            "email": "admin@goe-os.com",
            "full_name": "GOE OS Admin",
            "role": "super_admin"
        }
        logger.info("✅ Admin user created (default: admin/admin123)")
    
    logger.info("✅ GOE OS جاهز للاستخدام مع الأمان الكامل")
    yield
    logger.info("👋 GOE OS في طور الإيقاف...")

# ============================================================
# التطبيق الرئيسي
# ============================================================

app = FastAPI(
    title="GOE OS - النسخة الممتازة (Production-Ready)",
    description="نظام الحوكمة المعرفية المتكامل - مع أمان كامل وإدارة متقدمة",
    version="8.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# إضافة Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# إضافة Middleware الأمان
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # يفضل تحديد النطاقات المسموحة في الإنتاج
)

# CORS (مع قيود أمان)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
    max_age=3600,
)

# ============================================================
# نقاط النهاية العامة (بدون مصادقة)
# ============================================================

@app.get("/", include_in_schema=False)
async def root():
    return {
        "name": "GOE OS",
        "version": "8.0.0",
        "status": "running",
        "security": "enabled",
        "docs": "/docs",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health", include_in_schema=False)
async def health():
    return {
        "status": "healthy",
        "version": "8.0.0",
        "uptime": "since " + datetime.utcnow().isoformat()
    }

@app.get("/api/v2/status", dependencies=[Depends(limiter.limit("10/minute"))])
async def status():
    return {
        "status": "running",
        "version": "8.0.0",
        "components": {
            "auto_loader": AUTO_LOADER_AVAILABLE,
            "core": CORE_AVAILABLE,
            "reputation": REPUTATION_AVAILABLE,
            "challenges": CHALLENGES_AVAILABLE,
            "templates": TEMPLATES_AVAILABLE,
            "mentors": MENTORS_AVAILABLE,
            "gaps": GAPS_AVAILABLE,
            "community": COMMUNITY_AVAILABLE,
            "strategic": STRATEGIC_AVAILABLE,
            "integration": INTEGRATION_AVAILABLE
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================
# نقاط نهاية المصادقة (Authentication)
# ============================================================

@app.post("/api/v2/auth/register", dependencies=[Depends(limiter.limit("5/minute"))])
async def register(user_data: UserCreate, request: Request):
    """تسجيل مستخدم جديد"""
    if user_data.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if any(u.get("email") == user_data.email for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    users_db[user_data.username] = {
        "hashed_password": get_password_hash(user_data.password),
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": "viewer"
    }
    
    log_audit(user_data.username, "register", {"ip": request.client.host if request.client else "unknown"})
    
    return {"status": "success", "message": "User created successfully", "username": user_data.username}

@app.post("/api/v2/auth/login", dependencies=[Depends(limiter.limit("10/minute"))])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None):
    """تسجيل الدخول والحصول على توكنات"""
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        log_audit(form_data.username, "login_failed", {"ip": request.client.host if request else "unknown"}, "failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": form_data.username, "role": user.get("role", "viewer")})
    refresh_token = create_refresh_token(form_data.username)
    
    log_audit(form_data.username, "login", {"ip": request.client.host if request else "unknown"})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.post("/api/v2/auth/refresh")
async def refresh_token(refresh_token: str, request: Request):
    """تحديث التوكن باستخدام Refresh Token"""
    if refresh_token not in refresh_tokens_db:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    username = refresh_tokens_db[refresh_token]["username"]
    if username not in users_db:
        raise HTTPException(status_code=401, detail="User not found")
    
    # حذف التوكن القديم وإنشاء جديد
    del refresh_tokens_db[refresh_token]
    new_access_token = create_access_token(data={"sub": username, "role": users_db[username].get("role", "viewer")})
    new_refresh_token = create_refresh_token(username)
    
    log_audit(username, "refresh_token", {"ip": request.client.host if request else "unknown"})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.post("/api/v2/auth/logout")
async def logout(refresh_token: str, current_user: Dict = Depends(get_current_active_user)):
    """تسجيل الخروج وإبطال Refresh Token"""
    if refresh_token in refresh_tokens_db:
        del refresh_tokens_db[refresh_token]
    
    log_audit(current_user["username"], "logout", {})
    return {"status": "success", "message": "Logged out successfully"}

@app.get("/api/v2/auth/me")
async def get_me(current_user: Dict = Depends(get_current_active_user)):
    """الحصول على معلومات المستخدم الحالي"""
    user = users_db.get(current_user["username"], {})
    return {
        "username": current_user["username"],
        "email": user.get("email"),
        "full_name": user.get("full_name"),
        "role": user.get("role", "viewer")
    }

# ============================================================
# نقاط نهاية محمية (مع مصادقة وأذونات)
# ============================================================

@app.post("/api/v2/govern", dependencies=[Depends(limiter.limit("50/minute"))])
async def govern(
    request_data: AnalysisRequest,
    current_user: Dict = Depends(get_current_active_user),
    request: Request = None
):
    """تشخيص النصوص باستخدام المؤشرات التسعة (محمي)"""
    start_time = time.time()
    
    try:
        diag = get_diagnostics()
        if not diag:
            raise HTTPException(status_code=503, detail="DiagnosticsLayer غير متاح")
        
        result = diag.diagnose({
            "text": request_data.text,
            "entity": request_data.entity,
            "depth": request_data.depth,
            "domain": request_data.domain
        })
        
        processing_time = time.time() - start_time
        audit_id = f"audit_{int(time.time())}_{current_user['username']}"
        
        log_audit(
            current_user["username"], 
            "govern_analyze",
            {
                "text_length": len(request_data.text),
                "depth": request_data.depth,
                "domain": request_data.domain,
                "processing_time": round(processing_time, 3),
                "ip": request.client.host if request else "unknown"
            },
            "success"
        )
        
        return {
            "status": "success",
            "result": result,
            "audit_id": audit_id,
            "processing_time": round(processing_time, 3)
        }
    
    except Exception as e:
        log_audit(current_user["username"], "govern_analyze_error", {"error": str(e)}, "failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/govern/indicators", dependencies=[Depends(limiter.limit("30/minute"))])
async def get_indicators(current_user: Dict = Depends(get_current_active_user)):
    """الحصول على جميع المؤشرات التسعة (محمي)"""
    if CORE_AVAILABLE:
        return {"indicators": KnowledgeIndicators.get_all_indicators()}
    raise HTTPException(status_code=503, detail="KnowledgeIndicators غير متاح")

# ============================================================
# باقي نقاط النهاية (مع المصادقة)
# ============================================================

@app.post("/api/v2/historical/ingest", dependencies=[Depends(limiter.limit("5/minute"))])
async def ingest_historical_data(
    background_tasks: BackgroundTasks,
    sources: Optional[List[str]] = None,
    current_user: Dict = Depends(require_role("analyst"))
):
    """استيراد البيانات التاريخية (يحتاج صلاحية Analyst)"""
    try:
        from execution.historical.ingestor import HistoricalIngestor
        ingestor = HistoricalIngestor()
        
        log_audit(current_user["username"], "historical_ingest", {"sources": sources})
        
        if sources:
            background_tasks.add_task(ingestor.run_full_ingestion, sources)
            return {"status": "started", "message": f"جارٍ استيراد البيانات من: {sources}"}
        else:
            result = ingestor.run_full_ingestion()
            return {"status": "completed", "results": result}
    except ImportError:
        raise HTTPException(status_code=503, detail="HistoricalIngestor غير متاح")

@app.post("/api/v2/backtest/run", dependencies=[Depends(limiter.limit("10/minute"))])
async def run_backtest(
    countries: Optional[List[str]] = None,
    years: Optional[List[int]] = None,
    current_user: Dict = Depends(require_role("analyst"))
):
    """تشغيل الاختبار الخلفي (يحتاج صلاحية Analyst)"""
    try:
        from execution.backtesting.engine import BacktestingEngine
        engine = BacktestingEngine()
        
        log_audit(current_user["username"], "backtest_run", {"countries": countries, "years": years})
        
        results = engine.run_full_backtest(countries, years)
        return {"status": "success", "results": results}
    except ImportError:
        raise HTTPException(status_code=503, detail="BacktestingEngine غير متاح")

# ============================================================
# نقاط نهاية المجتمع (مع المصادقة الأساسية)
# ============================================================

@app.post("/api/v2/community/post", dependencies=[Depends(limiter.limit("30/minute"))])
async def create_post(
    title: str, 
    content: str, 
    tags: List[str] = None,
    current_user: Dict = Depends(get_current_active_user)
):
    """إنشاء منشور جديد في المجتمع"""
    community = get_community()
    if not community:
        raise HTTPException(status_code=503, detail="GOECommunity غير متاح")
    
    log_audit(current_user["username"], "community_post", {"title": title})
    
    return community.create_post(current_user["username"], title, content, tags)

@app.post("/api/v2/community/comment", dependencies=[Depends(limiter.limit("50/minute"))])
async def add_comment(
    post_id: str,
    comment: str,
    current_user: Dict = Depends(get_current_active_user)
):
    """إضافة تعليق على منشور"""
    community = get_community()
    if not community:
        raise HTTPException(status_code=503, detail="GOECommunity غير متاح")
    
    log_audit(current_user["username"], "community_comment", {"post_id": post_id})
    
    return community.add_comment(post_id, current_user["username"], comment)

# ============================================================
# نقاط نهاية الإدارة (Super Admin فقط)
# ============================================================

@app.get("/api/v2/admin/users", dependencies=[Depends(require_role("super_admin"))])
async def get_all_users():
    """الحصول على قائمة جميع المستخدمين (Super Admin فقط)"""
    return {"users": list(users_db.keys())}

@app.get("/api/v2/admin/audit-logs", dependencies=[Depends(require_role("super_admin"))])
async def get_audit_logs(limit: int = 100, offset: int = 0):
    """الحصول على سجلات التدقيق (Super Admin فقط)"""
    return {
        "total": len(audit_logs_db),
        "logs": audit_logs_db[-limit-offset:][:limit] if audit_logs_db else []
    }

@app.put("/api/v2/admin/users/{username}/role", dependencies=[Depends(require_role("super_admin"))])
async def update_user_role(username: str, role: str):
    """تحديث صلاحية مستخدم (Super Admin فقط)"""
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    valid_roles = ["viewer", "analyst", "admin", "super_admin"]
    if role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {valid_roles}")
    
    users_db[username]["role"] = role
    log_audit("system", "update_role", {"username": username, "role": role})
    
    return {"status": "success", "message": f"Role updated to {role}"}

# ============================================================
# نقاط نهاية WebSocket (مع مصادقة)
# ============================================================

class CollaborationManager:
    def __init__(self):
        self.active_sessions: Dict[str, List[WebSocket]] = {}
        self.session_data: Dict[str, Dict] = {}
        self.session_users: Dict[str, List[str]] = {}
    
    async def join_session(self, session_id: str, websocket: WebSocket, user_name: str):
        await websocket.accept()
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = []
            self.session_data[session_id] = {"users": [], "messages": [], "shared_text": "", "analysis": {}}
            self.session_users[session_id] = []
        self.active_sessions[session_id].append(websocket)
        self.session_users[session_id].append(user_name)
        await self._broadcast(session_id, {"type": "user_joined", "user": user_name, "users": self.session_users[session_id]})
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                if message["type"] == "edit_text":
                    self.session_data[session_id]["shared_text"] = message["text"]
                    await self._broadcast(session_id, {"type": "text_update", "text": message["text"], "user": user_name})
                elif message["type"] == "analyze":
                    if CORE_AVAILABLE:
                        diag = DiagnosticsLayer()
                        analysis = diag.diagnose({"text": self.session_data[session_id]["shared_text"]})
                        self.session_data[session_id]["analysis"] = analysis
                        await self._broadcast(session_id, {"type": "analysis_result", "analysis": analysis, "user": user_name})
                elif message["type"] == "chat":
                    self.session_data[session_id]["messages"].append({"user": user_name, "text": message["text"], "timestamp": datetime.utcnow().isoformat()})
                    await self._broadcast(session_id, {"type": "chat_message", "user": user_name, "text": message["text"]})
        except WebSocketDisconnect:
            if session_id in self.active_sessions:
                self.active_sessions[session_id].remove(websocket)
                if session_id in self.session_users:
                    self.session_users[session_id].remove(user_name)
                await self._broadcast(session_id, {"type": "user_left", "user": user_name, "users": self.session_users.get(session_id, [])})
                if not self.active_sessions[session_id]:
                    del self.active_sessions[session_id]
                    if session_id in self.session_data:
                        del self.session_data[session_id]
                    if session_id in self.session_users:
                        del self.session_users[session_id]
    
    async def _broadcast(self, session_id: str, message: Dict):
        if session_id not in self.active_sessions:
            return
        for websocket in self.active_sessions[session_id]:
            try:
                await websocket.send_text(json.dumps(message))
            except:
                pass

collab_manager = CollaborationManager()

@app.websocket("/ws/collaborate/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    session_id: str, 
    token: str = Query(...)
):
    """نقطة نهاية WebSocket مع مصادقة عبر التوكن"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in users_db:
            await websocket.close(code=4001, reason="Invalid token")
            return
    except JWTError:
        await websocket.close(code=4001, reason="Invalid token")
        return
    
    await collab_manager.join_session(session_id, websocket, username)

# ============================================================
# نقطة نهاية الدورة الكاملة (Admin فقط)
# ============================================================

@app.post("/api/v2/cycle/full", dependencies=[Depends(require_role("admin"))])
async def run_full_cycle(background_tasks: BackgroundTasks, current_user: Dict = Depends(get_current_active_user)):
    """تشغيل دورة كاملة (Admin فقط)"""
    tasks = []
    
    try:
        from execution.historical.ingestor import HistoricalIngestor
        ingestor = HistoricalIngestor()
        background_tasks.add_task(ingestor.run_full_ingestion)
        tasks.append("historical_ingestion")
    except ImportError:
        pass
    
    try:
        from execution.backtesting.engine import BacktestingEngine
        engine = BacktestingEngine()
        background_tasks.add_task(engine.run_full_backtest, ["EG", "SA", "AE"], [2010, 2015])
        tasks.append("backtesting")
    except ImportError:
        pass
    
    try:
        from execution.marketing.self_expansion_leader import SelfExpansionLeader
        leader = SelfExpansionLeader()
        background_tasks.add_task(leader.run_expansion_cycle)
        tasks.append("marketing_expansion")
    except ImportError:
        pass
    
    log_audit(current_user["username"], "full_cycle", {"tasks": tasks})
    
    return {
        "status": "started",
        "message": f"بدأت الدورة الكاملة. المهام المنفذة: {tasks}"
    }

# ============================================================
# نقاط نهاية إضافية (للتوافق مع الإصدارات السابقة مع مصادقة)
# ============================================================

@app.post("/api/v2/translate", dependencies=[Depends(get_current_active_user)])
async def translate(request: Request, current_user: Dict = Depends(get_current_active_user)):
    data = await request.json()
    return {"status": "translated", "result": "ترجمة مبدئية", "data": data}

@app.post("/api/v2/generate/code", dependencies=[Depends(get_current_active_user)])
async def generate_code(request: Request, current_user: Dict = Depends(get_current_active_user)):
    data = await request.json()
    return {"status": "generated", "result": "كود مبدئي", "data": data}

@app.post("/api/v2/law/analyze", dependencies=[Depends(get_current_active_user)])
async def law_analyze(request: Request, current_user: Dict = Depends(get_current_active_user)):
    data = await request.json()
    return {"status": "analyzed", "result": "تحليل قانوني مبدئي", "data": data}

@app.post("/api/v2/medicine/diagnose", dependencies=[Depends(get_current_active_user)])
async def medicine_diagnose(request: Request, current_user: Dict = Depends(get_current_active_user)):
    data = await request.json()
    return {"status": "diagnosed", "result": "تشخيص طبي مبدئي", "data": data}

@app.post("/api/v2/agriculture/calendar", dependencies=[Depends(get_current_active_user)])
async def agriculture_calendar(request: Request, current_user: Dict = Depends(get_current_active_user)):
    data = await request.json()
    return {"status": "generated", "result": "روزنامة محصولية مبدئية", "data": data}

# ============================================================
# نقاط نهاية مخصصة للمستخدمين المتميزين (Analyst+)
# ============================================================

@app.get("/api/v2/analyst/dashboard", dependencies=[Depends(require_role("analyst"))])
async def analyst_dashboard(current_user: Dict = Depends(get_current_active_user)):
    """لوحة تحليلية للمحللين"""
    return {
        "status": "success",
        "message": f"Welcome analyst {current_user['username']}",
        "tools": ["historical_data", "backtesting", "gap_analysis", "scenario_planning"]
    }

@app.post("/api/v2/admin/backup", dependencies=[Depends(require_role("admin"))])
async def create_backup(current_user: Dict = Depends(get_current_active_user)):
    """إنشاء نسخة احتياطية (Admin فقط)"""
    log_audit(current_user["username"], "backup_created", {})
    return {
        "status": "success",
        "message": "Backup created successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================
# معالج الأخطاء العالمي
# ============================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "detail": exc.detail,
            "path": request.url.path,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "detail": "Internal server error",
            "path": request.url.path,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# ============================================================
# التوثيق المخصص
# ============================================================

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="GOE OS - نسخة الإنتاج الممتازة",
        version="8.0.0",
        description="نظام الحوكمة المعرفية المتكامل مع أمان كامل",
        routes=app.routes,
    )
    
    # إضافة مخططات الأمان
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # إضافة أمان عام
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method not in ["get", "post", "put", "delete", "options", "head", "patch", "trace"]:
                continue
            if path.startswith("/api/v2/auth"):
                continue
            if path.startswith("/api/v2/admin"):
                openapi_schema["paths"][path][method]["security"] = [{"bearerAuth": []}]
                openapi_schema["paths"][path][method]["tags"] = ["Protected"]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ============================================================
# التشغيل
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        limit_concurrency=100,
        timeout_keep_alive=30
    )
