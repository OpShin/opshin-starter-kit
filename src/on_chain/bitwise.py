#!opshin
from opshin.prelude import *

@wraps_builtin
def integer_to_byte_string(big_endian: bool, width: int, val: int) -> bytes:
    """Returns the integer represented by a bytestring.
    Width controls the number of bytes used. If width is 0, the minimum number of bytes is used.
    Big_endian controls the endianness."""
    pass


@wraps_builtin
def byte_string_to_integer(big_endian: bool, a: bytes) -> int:
    """Returns the representation of an integer as a bytestring. Undoes integer_to_byte_string."""
    pass

@wraps_builtin
def xor_byte_string(pad: bool, a: bytes, b: bytes) -> bytes:
    """Logical XOR applied to two bytearrays. The first argument indicates whether padding semantics should be used. If this argument is False, truncation semantics are used instead."""
    pass



def validator(context: ScriptContext) -> None:
    """
    A contract that checks whether the bitwise AND of the datum and redeemer is zero.
    """
    datum: int = own_datum_unsafe(context)
    redeemer: int = context.redeemer
    datum_bytes = integer_to_byte_string(True, 0, datum)
    redeemer_bytes = integer_to_byte_string(True, 0, redeemer)
    # compute the bitwise AND of the two byte arrays
    xor_bytes = xor_byte_string(True, datum_bytes, redeemer_bytes)
    xor_int = byte_string_to_integer(True, xor_bytes)
    assert xor_int == 0, f"Expected bitwise XOR to be zero, but got {xor_int}"
