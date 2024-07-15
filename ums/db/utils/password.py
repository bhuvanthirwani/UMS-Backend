from ums.utils import hash_password


def hash_pswd_before_save(mapper, connection, target):
    """Event listener to hash the password before insert"""
    target.password = hash_password(target.password)
