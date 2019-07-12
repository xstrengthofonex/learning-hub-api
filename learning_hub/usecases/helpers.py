from uuid import uuid4


class IdGenerator:
    @staticmethod
    def generate():
        return str(uuid4())
