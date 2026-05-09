from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from core.config_manager import ConfigManager

router = APIRouter()
config_manager = ConfigManager()


class ConfigContent(BaseModel):
    content: str


class ConfigValidation(BaseModel):
    valid: bool
    message: str


class Backup(BaseModel):
    path: str
    name: str
    time: str


@router.get("/")
async def get_config():
    """Get configuration content"""
    try:
        content = config_manager.read_config()
        if content:
            return {"content": content}
        else:
            raise HTTPException(status_code=404, detail="Config file not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/")
async def save_config(config: ConfigContent):
    """Save configuration content"""
    try:
        success = config_manager.save_config(config.content)
        if success:
            return {"success": True, "message": "Config saved"}
        else:
            raise HTTPException(status_code=500, detail="Failed to save config")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate")
async def validate_config(config: ConfigContent):
    """Validate configuration content"""
    try:
        valid, message = config_manager.validate_config(config.content)
        return {"valid": valid, "message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/backup")
async def create_backup():
    """Create a backup of the configuration"""
    try:
        success = config_manager.create_backup()
        if success:
            return {"success": True, "message": "Backup created"}
        else:
            raise HTTPException(status_code=500, detail="Failed to create backup")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/backups", response_model=List[Backup])
async def list_backups():
    """List all backups"""
    try:
        backups = config_manager.list_backups()
        return backups
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/restore")
async def restore_backup(backup_path: str):
    """Restore a backup"""
    try:
        success = config_manager.restore_backup(backup_path)
        if success:
            return {"success": True, "message": "Backup restored"}
        else:
            raise HTTPException(status_code=500, detail="Failed to restore backup")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/format")
async def format_config(config: ConfigContent):
    """Format configuration content"""
    try:
        import json
        data = json.loads(config.content)
        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        return {"content": formatted}
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
