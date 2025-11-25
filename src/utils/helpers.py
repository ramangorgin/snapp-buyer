import time
import random
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def human_delay(min_seconds=1, max_seconds=3):
    """Add human-like random delay"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def retry_on_failure(max_retries=3, delay=2, backoff=2):
    """Decorator for retrying functions on failure"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"❌ Failed after {max_retries} retries: {e}")
                        raise
                    
                    wait_time = delay * (backoff ** (retries - 1))
                    logger.warning(f"🔄 Retry {retries}/{max_retries} after {wait_time}s - Error: {e}")
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator

def format_product_info(product):
    """Format product information for logging"""
    return f"📦 {product.get('name', 'Unknown')} - 💰 {product.get('price', 'N/A')}"

def is_within_time_range(start_time, end_time):
    """Check if current time is within specified range"""
    now = datetime.now().time()
    return start_time <= now <= end_time

def generate_session_id():
    """Generate unique session ID"""
    return f"session_{int(time.time())}_{random.randint(1000, 9999)}"