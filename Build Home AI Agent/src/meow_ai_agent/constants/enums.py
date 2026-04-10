from enum import Enum, auto

class RetStatus(Enum):
    SUCCESS = 0
    ERROR = -1


class IntentStatus(Enum):
    UNKNOW = "UNKNOW"
    TOOL = "TOOL"
    RAG = "RAG"
    WEB = "WEB"

    @classmethod
    def from_string(cls, value: str):
        try:
            return cls(value.upper())
        except ValueError:
            return cls.UNKNOW