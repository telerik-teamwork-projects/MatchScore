from fastapi import HTTPException


class BadRequest(HTTPException):
    def __init__(self, detail=''):
        super().__init__(status_code=400, detail=detail)


class NotFound(HTTPException):
    def __init__(self, detail=''):
        super().__init__(status_code=404, detail=detail)


class Unauthorized(HTTPException):
    def __init__(self, detail=''):
        super().__init__(status_code=401, detail=detail)


class Forbidden(HTTPException):
    def __init__(self, detail=''):
        super().__init__(status_code=403, detail=detail)


class InternalServerError(HTTPException):
    def __init__(self, detail=""):
        super().__init__(status_code=500, detail=detail)


class IntegrityError(HTTPException):
    def __init__(self, detail=''):
        super().__init__(status_code=400, detail=detail)