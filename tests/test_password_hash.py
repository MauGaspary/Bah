from app.utils.passwordHasher import PasswordHasher

def test_hash_password():
    hasher = PasswordHasher()
    password = "supersenha"
    hashed = hasher.hash(password)
    assert hashed != password
    assert hasher.verify(password, hashed)

def test_verify_correct_password():
    hasher = PasswordHasher()
    password = "supersenha"
    hashed = hasher.hash(password)
    assert hasher.verify(password, hashed)
    assert not hasher.verify("wrongpassword", hashed)

def test_verify_wrong_password():
    hasher = PasswordHasher()
    password = "supersenha"
    hashed = hasher.hash(password)
    assert not hasher.verify("wrongpassword", hashed)

def test_salt_unique():
    hasher = PasswordHasher()
    password = "supersenha"
    hashed1 = hasher.hash(password)
    hashed2 = hasher.hash(password)
    assert hashed1 != hashed2