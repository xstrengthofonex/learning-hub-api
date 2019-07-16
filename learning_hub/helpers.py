from uuid import uuid4

from datetime import datetime


class IdGenerator:
    @staticmethod
    def generate():
        return str(uuid4())


class Clock:
    @staticmethod
    def now() -> datetime:
        return datetime.now()
