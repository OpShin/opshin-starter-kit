import pytest
from opshin import compiler, Nothing
from opshin.ledger.api_v3 import Spending

from src.on_chain import vesting


@pytest.mark.parametrize("beneficiary", [b"00", b"11"])
@pytest.mark.parametrize("signatories", [[b"00", b"22"], [b"11", b"22"]])
def test_signed_by_beneficiary(beneficiary, signatories):
    res = vesting.signed_by_beneficiary(
        vesting.VestingParams(
            beneficiary,
            0,
        ),
        vesting.ScriptContext(
            vesting.TxInfo(
                [],
                [],
                [],
                0,
                {},
                [],
                {},
                vesting.POSIXTimeRange(
                    vesting.LowerBoundPOSIXTime(
                        vesting.NegInfPOSIXTime(), vesting.FalseData()
                    ),
                    vesting.UpperBoundPOSIXTime(
                        vesting.PosInfPOSIXTime(), vesting.FalseData()
                    ),
                ),
                signatories,
                {},
                {},
                vesting.TxId(b"00"),
                {},
                [],
                0,
                0,
            ),
            Nothing(),
            vesting.Spending(vesting.TxOutRef(vesting.TxId(b"00"), 0)),
        ),
    )
    assert res == (
        beneficiary in signatories
    ), "Invalid behaviour for signed_by_beneficiary"
