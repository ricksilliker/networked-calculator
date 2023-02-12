# models.py manages the datatypes that are passed between the client and server.
from dataclasses import dataclass, asdict


@dataclass
class ExpressionRequest(object):
    '''ExpressionRequest is the data that the client passes off to the server.'''
    expression: str

    def serialize(self):
        return asdict(self)


@dataclass
class ResultResponse(object):
    '''ResultResponse holds the answer to the expression passed in by the request.'''
    status_code: int
    answer: float

    def serialize(self):
        return asdict(self)


@dataclass
class ErrorResponse(object):
    '''ErrorResponse is the error object when an issue occurs with the expression on the server.'''
    status_code: int
    message: str

    def serialize(self):
        return asdict(self)
