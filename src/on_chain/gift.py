from eopsin.prelude import *


@dataclass()
class CancelDatum(PlutusData):
    pubkeyhash: bytes


def validator(datum: CancelDatum, redeemer: NoRedeemer, context: ScriptContext) -> None:
    sig_present = datum.pubkeyhash in context.tx_info.signatories
    assert sig_present, "Required signature missing"

