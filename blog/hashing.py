from passlib.context import CryptContext
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    # for hash
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    # for verify 
    def verify(hashed_password,plain_password):
        return pwd_cxt.verify(plain_password,hashed_password)