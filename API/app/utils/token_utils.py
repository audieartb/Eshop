from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

token_algo = URLSafeTimedSerializer(
    SECRET_KEY, salt='Order_Verification_Email')


def token(email: str, order_id: str):
    to_dump = {
        "email": email,
        "order_id": order_id
    }

    _token = token_algo.dumps(to_dump)
    return _token


def verify_token(token: str):
    try:
        data = token_algo.loads(token, max_age=18000)
        
    except SignatureExpired:
        return None
    except BadTimeSignature:
        return None
    return {'data': data, 'check': True}
