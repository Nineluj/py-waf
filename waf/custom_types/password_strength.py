from enum import Enum


class PasswordStrength(Enum):
    """Level of password strengths"""
    TOO_GUESSABLE = 0
    VERY_GUESSABLE = 1
    SOMEWHAT_GUESSABLE = 2
    SAFELY_UNGUESSABLE = 3
    VERY_UNGUESSABLE = 4