# app utility files.
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password):
    """Hash the password before saving"""
    return generate_password_hash(password=password)



def match_password(db_pswd, password: str) -> bool:
    """Matches user password with database password"""
    #print(f"check_password_hash(pwhash=db_pswd, password=password): {check_password_hash(pwhash=db_pswd, password=password)}, {db_pswd} {password}")
    return bool(check_password_hash(pwhash=db_pswd, password=password))
