import web3 as w3


def authenticate_user(public_key, signature, message):
    msg_hash = w3.keccak(text=message)
    try:
        recovered = w3.eth.account.recoverHash(msg_hash, signature=signature)
    except ValueError:
        return False
    return recovered == public_key