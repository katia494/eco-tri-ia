import time
from fastapi import Request
from backend.api.logger import logger

async def log_requests(request: Request, call_next):
    """
    Middleware qui log chaque requête avec son temps de réponse.
    """
    start_time = time.time()
    
    logger.info(f"→ {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    duration = round((time.time() - start_time) * 1000, 2)
    
    logger.info(
        f"← {request.method} {request.url.path} "
        f"| Status: {response.status_code} "
        f"| Durée: {duration}ms"
    )
    
    return response