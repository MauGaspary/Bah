class DomainException(Exception):
    pass


class EmailAlreadyExistsException(DomainException):
    pass


class InvalidCredentialsException(DomainException):
    pass


class ResourceNotFoundException(DomainException):
    pass


# --- ADIÇÃO (para compatibilizar com o repo que importa ResourceNotFound) ---
class ResourceNotFound(ResourceNotFoundException):
    """Alias compatível para NotFound usado no repositório."""

    pass
