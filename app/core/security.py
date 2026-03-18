from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    pwd = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(pwd)