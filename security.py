from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    """
    Function that gets called when a user calls the /auth endpoint
    with their username and password
    :param username: username in string format
    :param password: user un-encrypted password in string format
    :return: a user if auth is successful, none otherwise
    """
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user
    return None

def identity(payload):
    """
    Function that gets called when user has already authenticated, and flask_JWT
    verified theri atuhorisation header is correct
    :param payload: A dict with "identity" key, which is the user ID
    :return: A userModel object.
    """

    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)