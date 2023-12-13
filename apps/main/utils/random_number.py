import random
import string


def random_number(length=10) -> int:
    """Create a random number

    Args:
        length (int, optional): length of number. Defaults to 10.

    Returns:
        int: random number
    """
    return int(''.join(random.choices(
            string.digits,
            k=length
        )
    ))