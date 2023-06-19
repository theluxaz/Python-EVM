

def unsigned_to_signed(value: int) -> int:
    if value <= (2**256 - 1):
        return value
    else:
        return value - (2**256)


def signed_to_unsigned(value: int) -> int:
    if value < 0:
        return value + (2**256)
    else:
        return value