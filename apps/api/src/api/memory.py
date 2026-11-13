from fastapi import APIRouter, HTTPException
import httpx
from pydantic import BaseModel
import uuid
from typing import Optional
from src.config import get_settings

router = APIRouter()

class PreferencePayload(BaseModel):
    id: Optional[str] = None
    category: str
    key: str
    value: str
    confidence: float = 1.0

class FactPayload(BaseModel):
    id: Optional[str] = None
    fact: str
    category: Optional[str] = None
    confidence: float = 1.0

@router.get("/preferences")
async def get_preferences():
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            headers = {
                "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
            }
            resp = await client.get(f"{settings.SUPABASE_URL}/rest/v1/user_preferences?order=learned_at.desc", headers=headers)
            if resp.status_code == 200:
                return resp.json()
            return []
    except Exception:
        return []

@router.post("/preferences")
async def save_preference(payload: PreferencePayload):
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            headers = {
                "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
            data = {
                "id": payload.id or str(uuid.uuid4()),
                "user_id": "00000000-0000-0000-0000-000000000000",
                "category": payload.category,
                "key": payload.key,
                "value": payload.value,
                "confidence": payload.confidence
            }
            resp = await client.post(f"{settings.SUPABASE_URL}/rest/v1/user_preferences", headers=headers, json=data)
            return data
    except Exception:
        return {
            "id": payload.id or str(uuid.uuid4()),
            "user_id": "00000000-0000-0000-0000-000000000000",
            "category": payload.category,
            "key": payload.key,
            "value": payload.value,
            "confidence": payload.confidence
        }

@router.delete("/preferences/{id}")
async def delete_preference(id: str):
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            headers = {
                "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
            }
            await client.delete(f"{settings.SUPABASE_URL}/rest/v1/user_preferences?id=eq.{id}", headers=headers)
    except Exception:
        pass
    return {"status": "success"}

@router.get("/facts")
async def get_facts():
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            headers = {
                "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
            }
            resp = await client.get(f"{settings.SUPABASE_URL}/rest/v1/memory_facts?order=created_at.desc", headers=headers)
            if resp.status_code == 200:
                return resp.json()
            return []
    except Exception:
        return []

@router.post("/facts")
async def save_fact(payload: FactPayload):
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            headers = {
                "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            }
            data = {
                "id": payload.id or str(uuid.uuid4()),
                "user_id": "00000000-0000-0000-0000-000000000000",
                "fact": payload.fact,
                "category": payload.category,
                "confidence": payload.confidence
            }
            await client.post(f"{settings.SUPABASE_URL}/rest/v1/memory_facts", headers=headers, json=data)
            return data
    except Exception:
        return {
            "id": payload.id or str(uuid.uuid4()),
            "user_id": "00000000-0000-0000-0000-000000000000",
            "fact": payload.fact,
            "category": payload.category,
            "confidence": payload.confidence
        }

@router.delete("/facts/{id}")
async def delete_fact(id: str):
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            headers = {
                "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
            }
            await client.delete(f"{settings.SUPABASE_URL}/rest/v1/memory_facts?id=eq.{id}", headers=headers)
    except Exception:
        pass
    return {"status": "success"}
