import bcrypt


class PasswordHasher:
    def __init__(self):
        self.rounds = 13

    def hash(self, password: str) -> str:
        salt = bcrypt.gensalt(self.rounds)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
