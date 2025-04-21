from enum import Enum as PyEnum


class UserRole(PyEnum):
    ADMIN = "ROLE_ADMIN"
    USER = "ROLE_USER"

class State(PyEnum):
    booked = "booked"
    cancelled = "cancelled"
    passed = "passed"