import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_TTL = int(os.getenv("JWT_TTL"))
JWT_ISS = os.getenv("JWT_ISS")
ALGORITHM = "HS256"