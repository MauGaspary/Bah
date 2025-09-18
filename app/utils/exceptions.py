class DomainException(Exception):
    pass


class EmailAlreadyExistsException(DomainException):
    pass


class InvalidCredentialsException(DomainException):
    pass


class ResourceNotFoundException(DomainException):
    pass
