from enum import Enum


class RequestType(Enum):
    """Types of requests"""
    DEFAULT = 0
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4
    OPTIONS = 5
    HEAD = 6
    TRACE = 7
    PATCH = 8
    CONNECT = 9
