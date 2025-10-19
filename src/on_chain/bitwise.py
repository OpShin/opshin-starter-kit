#!opshin
from opshin.prelude import *
from opshin.std.math import *


@dataclass
class BitwiseDatum(PlutusData):
    """
    A datum that holds an integer value for bitwise operations
    and a owner
    """
    CONSTR_ID = 0
    value: int
    owner: PubKeyHash

def signed_by_owner(owner: PubKeyHash, context: ScriptContext) -> bool:
    return owner in context.tx_info.signatories

EIGHT_BIT_POWERS = [1, 2, 4, 8, 16, 32, 64, 128]

def xor_8bit(a: int, b: int) -> int:
    result = 0
    for power in EIGHT_BIT_POWERS:
        bit_a = (a // power) % 2
        bit_b = (b // power) % 2
        bit_and = (bit_a + bit_b) % 2
        result = result + bit_and * power
    return result


def xor_bytestring(a: bytes, b: bytes) -> bytes:
    """Returns the bitwise AND of two bytestrings, padding the shorter one with leading zeros"""
    max_len = max([len(a), len(b)])
    a = a.rjust(max_len, b"\x00")
    b = b.rjust(max_len, b"\x00")
    c = b""
    for i in range(max_len):
        j = max_len - i - 1
        c = cons_byte_string(xor_8bit(a[j], b[j]), c)
    return c


def validator(datum: BitwiseDatum, redeemer: int, context: ScriptContext) -> None:
    """
    A contract that checks whether the bitwise AND of the datum and redeemer is zero.
    """
    datum_bytes = bytes_big_from_unsigned_int(datum.value)
    redeemer_bytes = bytes_big_from_unsigned_int(redeemer)
    # compute the bitwise AND of the two byte arrays
    xor_bytes = xor_bytestring(datum_bytes, redeemer_bytes)
    xor_int = unsigned_int_from_bytes_big(xor_bytes)
    assert xor_int == 0, f"Expected bitwise XOR to be zero, but got {xor_int}"
    assert signed_by_owner(datum.owner, context), "beneficiary's signature missing"
