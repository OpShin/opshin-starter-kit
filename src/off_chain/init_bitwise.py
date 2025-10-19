import time

import click
from pycardano import (
    OgmiosChainContext,
    TransactionBuilder,
    TransactionOutput,
    VerificationKeyHash, Network,
)

from src.on_chain import vesting
from src.on_chain.bitwise import BitwiseDatum
from src.utils import get_signing_info, get_address, ogmios_url, network, kupo_url
from src.utils.contracts import get_contract
from src.utils.network import get_chain_context


@click.command()
@click.argument("name")
@click.argument("challenge")
@click.argument("beneficiary_name")
@click.option(
    "--amount",
    type=int,
    default=3000000,
    help="Amount of lovelace to send to the script address.",
)
def main(name: str, challenge: str, beneficiary_name: str, amount: int):
    # Load chain context
    context = get_chain_context()

    # Get payment address
    payment_address = get_address(name)
    beneficiary = get_signing_info(beneficiary_name)[0].hash().to_primitive()

    # Create the vesting datum
    params = int(challenge, 2)

    _, _, script_address = get_contract("bitwise")

    # Make datum
    datum = BitwiseDatum(
        value=params,
        owner=beneficiary,
    )

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
    if network == Network.TESTNET:
        print(f"Cexplorer: https://preprod.cexplorer.io/tx/{signed_tx.id}")
    else:
        print(f"Cexplorer: https://cexplorer.io/tx/{signed_tx.id}")


if __name__ == "__main__":
    main()
