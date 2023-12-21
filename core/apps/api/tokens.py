from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from django.conf import settings
from jwt.exceptions import PyJWTError


def encode_token(
    payload: dict = None,
    key: str = settings.SIMPLE_JWT["SIGNING_KEY"],
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
        payload (dict): A dictionary containing the payload data to be included in the token.
        Default is an empty dictionary.
        key (str): The secret key to use for encoding the token. Default is the value of the JWT_SIGNING_KEY setting.
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
            key=key,
            algorithm=settings.SIMPLE_JWT["ALGORITHM"],
        )
    except PyJWTError as error:
        raise ValueError(error)
    return str(token)


def decode_token(
    token: str,
    key: str = settings.SIMPLE_JWT["SIGNING_KEY"],
):
    """
    Decodes a token and returns its payload.
    Args:
        token (str): The token to decode.
        key (str): The key to use for decoding the token.
    Returns:
        dict: The payload of the decoded token.
    Raises:
        jwt.PyJWTError: If the token has an invalid signature.
    """
    try:
        payload = jwt.decode(
            jwt=token,
            key=key,
            algorithms=[settings.SIMPLE_JWT["ALGORITHM"]],
        )
        return payload
    except PyJWTError as error:
        raise ValueError(error)
