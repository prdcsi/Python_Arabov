from functools import wraps
from exceptions import PermissionDeniedError

def check_permissions(required_role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = kwargs.get("user_role") or (args[1] if len(args) > 1 else None)
            if user_role != required_role:
                raise PermissionDeniedError(f"Требуются права '{required_role}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator