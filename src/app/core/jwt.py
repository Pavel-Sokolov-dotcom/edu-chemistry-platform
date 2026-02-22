import jwt
from src.app.core.config import settings
from datetime import timedelta, datetime



def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Создаю JWT токен.
    
    Эта функция принимает на вход аргументы
    Args:
    data данные для включения в токен.
    expires_delta время жизни токена.
    
    Возвращает JWT токен строкой
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Проверяю валидность JWT токена.
    
    Args:
        token: JWT токен.
        
    Returns:
        dict: Данные из токена если валиден
        None: Если токен невалиден
    """
    try:    
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Токен JWT истёк")
        return None
    except jwt.InvalidTokenError:
        print("Невалидный JWT токен")
        return None
    