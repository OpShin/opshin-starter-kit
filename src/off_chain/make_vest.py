import subprocess
import time
from pathlib import Path

import click
from pycardano import (
    OgmiosChainContext,
    Address,
    TransactionBuilder,
    TransactionOutput,
    VerificationKeyHash,
)

from src.on_chain import vesting
from src.utils import get_signing_info, get_address, ogmios_url, network, kupo_url


@click.command()
@click.argument("name")
@click.argument("beneficiary")
@click.option(
    "--amount",
    type=int,
    default=3000000,
    help="Amount of lovelace to send to the script address.",
)
@click.option(
    "--wait_time",
    type=int,
    default=0,
    help="Time until the vesting contract deadline from current time",
)
def main(name: str, beneficiary: str, amount: int, wait_time: int):
    # Load chain context
    context = OgmiosChainContext(ogmios_url, network=network, kupo_url=kupo_url)

    # Get payment address
    payment_address = get_address(name)

    # Get the beneficiary VerificationKeyHash (PubKeyHash)
    beneficiary_address = get_address(beneficiary)
    vkey_hash: VerificationKeyHash = beneficiary_address.payment_part

    # Create the vesting datum
    params = vesting.VestingParams(
        beneficiary=bytes(vkey_hash),
        deadline=int(time.time() + wait_time) * 1000,  # must be in milliseconds
    )

    script_path = Path("./build/vesting/testnet.addr")

    # Load script info
    with open(script_path) as f:
        script_address = Address.from_primitive(f.read())

    # Make datum
    datum = params

    # Build the transaction
    builder = TransactionBuilder(context)
    builder.add_input_address(payment_address)
    builder.add_output(
        TransactionOutput(address=script_address, amount=amount, datum=datum)
    )

    # Sign the transaction
    payment_vkey, payment_skey, payment_address = get_signing_info(name)
    signed_tx = builder.build_and_sign(
        signing_keys=[payment_skey],
        change_address=payment_address,
    )

    # Submit the transaction
    context.submit_tx(signed_tx.to_cbor())

    print(f"transaction id: {signed_tx.id}")
    print(f"Cardanoscan: https://preview.cexplorer.io/tx/{signed_tx.id}")


if __name__ == "__main__":
    main()
