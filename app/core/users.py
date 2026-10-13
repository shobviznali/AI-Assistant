from app.core.password import hash_password

USERS = {
    "alice": {
        "hashed_password": hash_password("alice123")
    },
    "bob": {
        "hashed_password": hash_password("bob123")
    }
}