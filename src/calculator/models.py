from dataclasses import dataclass, asdict


@dataclass
class ExpressionRequest(object):
    expression: str


@dataclass
class ResultResponse(object):
    status_code: int
    answer: float

    def serialize(self):
        return asdict(self)


@dataclass
class ErrorResponse(object):
    status_code: int
    message: str

    def serialize(self):
        return asdict(self)
