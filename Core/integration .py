"""
طبقة التكامل (Webhooks, API Keys)
"""
from fastapi import APIRouter, Request
from typing import Dict, List, Optional
import hmac, hashlib
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2/integration", tags=["Integration"])

class IntegrationLayer:
    def __init__(self):
        self.webhooks = {}
        self.api_keys = {}
    
    def register_webhook(self, event: str, url: str, secret: str = None) -> Dict:
        self.webhooks[event] = {"url": url, "secret": secret, "registered_at": datetime.utcnow().isoformat(), "trigger_count": 0}
        return {"status": "registered", "event": event, "webhook": self.webhooks[event]}
    
    def trigger_webhook(self, event: str, data: Dict) -> Dict:
        if event not in self.webhooks:
            return {"status": "error", "message": f"لا يوجد Webhook للحدث {event}"}
        self.webhooks[event]["trigger_count"] += 1
        self.webhooks[event]["last_triggered"] = datetime.utcnow().isoformat()
        logger.info(f"📨 Webhook {event} triggered")
        return {"status": "triggered", "event": event, "data": data}
    
    def generate_api_key(self, app_name: str, permissions: List[str] = None) -> Dict:
        key_id = f"key_{app_name}_{int(datetime.utcnow().timestamp())}"
        secret = hmac.new(key_id.encode(), app_name.encode(), hashlib.sha256).hexdigest()
        self.api_keys[key_id] = {"app_name": app_name, "secret": secret, "permissions": permissions or ["read", "write"], "created_at": datetime.utcnow().isoformat()}
        return {"status": "created", "key_id": key_id, "secret": secret}
    
    def validate_api_key(self, key_id: str, secret: str) -> bool:
        if key_id not in self.api_keys:
            return False
        return self.api_keys[key_id]["secret"] == secret

@router.post("/webhook/register")
async def register_webhook(event: str, url: str, secret: Optional[str] = None):
    integration = IntegrationLayer()
    return integration.register_webhook(event, url, secret)

@router.post("/webhook/trigger/{event}")
async def trigger_webhook(event: str, data: Dict):
    integration = IntegrationLayer()
    return integration.trigger_webhook(event, data)

@router.post("/api-key/generate")
async def generate_api_key(app_name: str, permissions: List[str] = None):
    integration = IntegrationLayer()
    return integration.generate_api_key(app_name, permissions)

@router.get("/api-key/validate")
async def validate_api_key(key_id: str, secret: str):
    integration = IntegrationLayer()
    return {"valid": integration.validate_api_key(key_id, secret)}
