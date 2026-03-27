from enum import StrEnum

class ErrorSlug(StrEnum):
    NOT_FOUND =  "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    CONFLICT = "conflict"
    UNPROCESSABLE = "unprocessable"


class MutuoException(Exception):
    def __init__(self, detail: str, slug: ErrorSlug):
        super().__init__(detail)
        self.detail = detail
        self.slug = slug


class NotfoundException(MutuoException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, slug=ErrorSlug.NOT_FOUND)


class UnauthorizedException(MutuoException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail=detail, slug=ErrorSlug.UNAUTHORIZED)


class ForbiddenException(MutuoException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(detail=detail, slug=ErrorSlug.FORBIDDEN)


class ConflictException(MutuoException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(detail=detail, slug=ErrorSlug.CONFLICT)


class UnprocessableException(MutuoException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(detail=detail, slug=ErrorSlug.UNPROCESSABLE)