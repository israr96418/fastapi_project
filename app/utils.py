from passlib.context import CryptContext

psw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hasing(user_password: str):
    psw_hasing = psw_context.hash(user_password)
    return psw_hasing


def verify_password_of_user(plane_passw, hash_passw):
    print(plane_passw, "And Already hashpssword that is stored in database", hash_passw)
    # we can pass 2 argumnts to the verify function the first one should be the passwrd that we can convert into
    # hash and the 2nd one is that is already stored in the datbase
    # if we pass differnt pattrn than it will create ("interna derver error")
    matching_of_psswrd = psw_context.verify(plane_passw, hash_passw)
    return matching_of_psswrd
