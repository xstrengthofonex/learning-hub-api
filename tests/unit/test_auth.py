from uuid import uuid4

from learning_hub.auth import JWTAuth


USER_ID = str(uuid4())
SECRET = "Secret"


def test_generates_valid_jwt_token():
    jwt_auth = JWTAuth("Secret")
    token = jwt_auth.generate_token(USER_ID)
    result = jwt_auth.get_payload(token)
    assert result.get("userId") == USER_ID
