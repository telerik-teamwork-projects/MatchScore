from fastapi import Response


class RequestOK(Response):
    def __init__(self, content=''):
        super().__init__(status_code=200, content=content)


class RequestCreate(Response):
    def __init__(self, content=''):
        super().__init__(status_code=201, content=content)


class RequestNoContent(Response):
    def __init__(self, content=''):
        super().__init__(status_code=204, content=content)