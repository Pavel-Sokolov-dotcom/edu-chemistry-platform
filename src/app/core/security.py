import bcrypt  # ! Это работает, но надо понять почему помечен, как ошибка


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return (
        hashed.decode()
    )  # Возвращаю захешированный пароль, преобразованный из bytes в str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )  # Метод verify сам сравнивает хеши паролей
    except (ValueError, TypeError):
        return False
