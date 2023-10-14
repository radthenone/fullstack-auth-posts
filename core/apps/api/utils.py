import jwt
from datetime import datetime, timedelta
from uuid import uuid4
from django.conf import settings


def encode_token(
    payload: dict = None,
    headers: dict = None,
    exp_weeks: int = 0,
    exp_days: int = 0,
    exp_hours: int = 0,
    exp_minutes: int = 0,
    exp_seconds: int = 0,
):
    """
    Encodes a token with the given payload and expiration times.
    Parameters:
        payload (dict): A dictionary containing the payload data to be included in the token. Default is an empty dictionary.
        headers (dict): A dictionary. Default is an empty dictionary.
        exp_weeks (int): The number of weeks until the token expires. Default is 0.
        exp_days (int): The number of days until the token expires. Default is 0.
        exp_hours (int): The number of hours until the token expires. Default is 0.
        exp_minutes (int): The number of minutes until the token expires. Default is 5.
        exp_seconds (int): The number of seconds until the token expires. Default is 0.
    Returns:
        str: The encoded token as a string.
    Raises:
        ValueError: If there is an error encoding the token.
    """
    if all(item is None for item in (payload, headers)):
        payload, headers = {}, {}
    if all(
        value == 0
        for value in [
            exp_weeks,
            exp_days,
            exp_hours,
            exp_minutes,
            exp_seconds,
        ]
    ):
        exp_minutes = 5

    basic_payload = {
        "exp": datetime.utcnow()
        + timedelta(
            weeks=exp_weeks,
            days=exp_days,
            hours=exp_hours,
            minutes=exp_minutes,
            seconds=exp_seconds,
        ),
        "iat": datetime.utcnow(),
        "jti": uuid4().hex,
    }
    if payload is not None:
        basic_payload.update(payload)
    try:
        token = jwt.encode(
            payload=basic_payload,
            headers=headers,
            key=settings.SIMPLE_JWT["SIGNING_KEY"],
            algorithm=settings.SIMPLE_JWT["ALGORITHM"],
        )
    except ValueError as error:
        return {"errors": str(error)}
    return str(token)


def decode_token(token: str):
    """
    Decodes a token and returns its payload.
    Args:
        token (str): The token to decode.
    Returns:
        dict: The payload of the decoded token.
    Raises:
        jwt.InvalidSignatureError: If the token has an invalid signature.
    """
    _token = handle_expired_token(token)
    if isinstance(_token, dict):
        return _token
    else:
        try:
            payload = jwt.decode(
                jwt=_token,
                key=settings.SIMPLE_JWT["SIGNING_KEY"],
                algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
            )
        except jwt.InvalidSignatureError:
            payload = {"errors": "Invalid token"}
        return payload


def handle_expired_token(token: str):
    payload = jwt.decode(
        jwt=token,
        key=settings.SIMPLE_JWT["SIGNING_KEY"],
        algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
        options={"verify_signature": False},
    )
    now = datetime.now()
    exp_datetime = datetime.fromtimestamp(payload.get("exp"))
    iat_datetime = datetime.fromtimestamp(payload.get("iat"))
    if iat_datetime <= now <= exp_datetime:
        return token
    else:
        return {"errors": "Token has expired"}


def headers_token(token: str):
    return jwt.get_unverified_header(token)
