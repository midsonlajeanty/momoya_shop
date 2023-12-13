import string
import random


def random_string(length=10) -> str:
    """Create a random string

    Args:
        length (int, optional): length of string . Defaults to 10.

    Returns:
        str: random string
    """
    return ''.join(random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )
