import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"Request {request.method} {request.url.path} completed in {process_time:.2f}ms with status {response.status_code}")
    return response
