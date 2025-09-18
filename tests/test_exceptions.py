from app.utils.exceptions import (
    DomainException,
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    ResourceNotFoundException,
)


def test_domain_exception():
    exc = DomainException("Test message")
    assert str(exc) == "Test message"
    assert isinstance(exc, Exception)


def test_email_already_exists_exception():
    exc = EmailAlreadyExistsException("Email already exists")
    assert str(exc) == "Email already exists"
    assert isinstance(exc, DomainException)


def test_invalid_credentials_exception():
    exc = InvalidCredentialsException("Invalid credentials")
    assert str(exc) == "Invalid credentials"
    assert isinstance(exc, DomainException)


def test_resource_not_found_exception():
    exc = ResourceNotFoundException("Resource not found")
    assert str(exc) == "Resource not found"
    assert isinstance(exc, DomainException)
