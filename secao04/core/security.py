from passlib.context import CryptContext


CRIPT_CONTEXT = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def verify_password(password: str, hashed_password: str) -> bool:
    return CRIPT_CONTEXT.verify(password, hashed_password)

def generate_password_hash(password: str) -> str:
    return CRIPT_CONTEXT.hash(password)
