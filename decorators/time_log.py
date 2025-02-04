import time
from functools import wraps

# 2. Decorator
def timed_and_logged(title: str, description: str, log_file="execution_times.log"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                execution_time = end_time - start_time
                log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {title}: {description}, Tempo de execução: {execution_time:.0f} segundos\n"
                try:
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(log_message)
                except Exception as e:
                    print(f"Error writing to log file: {e}")

        return wrapper
    return decorator