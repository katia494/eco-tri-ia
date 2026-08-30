import time
from fastapi import Request
from backend.api.logger import logger
from backend.api.monitoring import monitoring_registry

async def log_requests(request: Request, call_next):
    """
    Middleware qui log chaque requête avec son temps de réponse.
    """
    start_time = time.time()
    
    logger.info(f"→ {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception:
        status_code = 500
        raise
    finally:
        duration = round((time.time() - start_time) * 1000, 2)
        monitoring_registry.record(
            request.method, request.url.path, status_code, duration
        )
        logger.info(
            f"← {request.method} {request.url.path} "
            f"| Status: {status_code} "
            f"| Durée: {duration}ms"
        )
