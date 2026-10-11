"""Authorization helpers.

Important: enforce permissions in application code before retrieval.
Never rely on the LLM prompt as an access-control mechanism.
"""

USER_GROUPS = {
    "alice": {"procurement"},
    "bob": {"hr"},
}

def user_can_access(username: str, owner_group: str) -> bool:
    return owner_group in USER_GROUPS.get(username.lower(), set())
