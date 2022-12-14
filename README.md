# Pycardano Starter-kit

This Starter-Kit is a simple implementation of the [PyCardano](https://github.com/Python-Cardano/pycardano) library, showing how you can use it for generating addresses, querying an address utxos and submit a basic transaction to transfer ADA in between 2 addresses.

PyCardano is a Cardano library written in Python. It allows users to create and sign transactions without depending on third-party Cardano serialization tools, such as cardano-cli and cardano-serialization-lib, making it a lightweight library, which is simple and fast to set up in all types of environments.

## Dev Environment

For executing the scripts in this starter kit you'll need access to a running [Ogmios](https://ogmios.dev/) instance.

In case you don't want to install the required components yourself, you can use [Demeter.run](https://demeter.run) platform to create a cloud environment with access to common Cardano infrastructure. The following command will open this repo in a private, web-based VSCode IDE with access to a running Ogmios instance in the preview network.

[![Code in Cardano Workspace](https://demeter.run/code/badge.svg)](https://demeter.run/code?repository=https://github.com/txpipe/pycardano-starter-kit&template=python)


## What is Included

We have included 3 python scripts for executing specific actions:

| Name                 | Description                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| `address_generator.py`              | generates an address together with its signing and verification keys                        |
| `address_utxos.py`             | Queries the utxos associated to an address input by the user                |
| `execute_transaction.py`             | Executes a basic transaction in between 2 addresses input by the user          |


## Running the scripts

The first step for running any of the scripts would be to install the dependencies. For doing that open a new terminal in the Development workspace and execute the following command:

```bash
pip install pycardano
```

### Generating an Address

For generating a new address we are going to run the `address_generator` script. 

The files with the associated keys will be generated in the path specified in the constant:

```python
PAYMENT_SIGNING_KEY_PATH = 'payment.skey'
PAYMENT_VERIFICATION_KEY_PATH = 'payment.vkey'
```

For running the script open a new terminal window from the workspace and execute:
```bash
python3 address_generator.py
```

The output of the script will be a generated address and 2 files should have been generated. `payment.skey` and `payment.vkey`

### Querying Address utxos

For querying the address utxo we are going to run the `address_uxtos` script.

This script requires that we build an `OgmiosChainContext` for querying the information.  For building this context we are going to use the Ogmios instance provided by [Demeter.run](https://demeter.run). 

Inside the Development workspace the information we require to build the `ws_url` parameter required by PyCardano is already available as environment variables inside `OGMIOS_HOST` and `OGMIOS_PORT`

```python
from pycardano import *
import os

def build_context(network: Network) -> OgmiosChainContext:
    ws_url = f"ws://{os.environ['OGMIOS_HOST']}:{os.environ['OGMIOS_PORT']}"
    return OgmiosChainContext(ws_url, network)
```

By using the function is now easy to query on-chain data from our scripts:

```python
context = build_context(Network.TESTNET)
utxos = context.utxos(address)
```

This script will require the user to input an address and outputs the uxtos associated as an array. If your address is newly generated you will see an empty array as the output of the terminal. 

For running the script from the workspace terminal execute the following command:
```bash
python3 address_utxos.py
```

You can request some test ADA by using a [testnet faucet](https://docs.cardano.org/cardano-testnet/tools/faucet).

After you have some utxos associated to your address the output from this script will look similar to this:
```bash
[{'input': {
  'index': 1,
  'transaction_id': TransactionId(hex='c2648468efe4886482009fef5510194c0f99bc56fa2a0e9f1f68fff02185affd'),
},
 'output': {
  'address': addr_test1vpyppmsrdrtedg4p2wwparp5artww6dcyw54r6dc8q4ryvshvkyyr,
  'amount': {'coin': 9989370535, 'multi_asset': {}},
  'datum': None,
  'datum_hash': None,
  'post_alonzo': False,
  'script': None,
}}]
```

### Executing a simple transaction

For executing a transaction we are going to use the `execute_transaction` script.

In a similar way to the script for querying the address utxos we will be using the Ogmios instance provided by Demeter.run for building, signing and submitting the transaction. 

For running the script from the workspace terminal execute the following command:
```bash
python3 execute_transaction.py
```

The script will first ask for the source address. Make sure this address has some tADA available to transfer. 
Then it will ask for the path of the source address signing key. If we are using an address generated with the `address_generator` script this value would be `payment.skey`
Finally it will ask for the destination address. 

```bash
Enter source address: addr_test1vpyppmsrdrtedg4p2wwparp5artww6dcyw54r6dc8q4ryvshvkyyr
Enter the name of the file with the signing key: payment.skey
Enter destination address: addr_test1vp4v2u7f3ssd3mrfh6ff3xz9304npg6fsevh9sh9sud3jfcdtgz8s
transaction fc41b4aa72367cb6c20cc3f3c34749522486baa5c434bbe2a6e5c4df1dba230f submitted
```

If the transaction was correctly submitted it will output in the terminal the id of the transaction. 

You can verify the destination address utxos after executing the transaction with the `address_utxos` script. 

```bash
[{'input': {
  'index': 0,
  'transaction_id': TransactionId(hex='c2648468efe4886482009fef5510194c0f99bc56fa2a0e9f1f68fff02185affd'),
},
 'output': {
  'address': addr_test1vp4v2u7f3ssd3mrfh6ff3xz9304npg6fsevh9sh9sud3jfcdtgz8s,
  'amount': {'coin': 10000000, 'multi_asset': {}},
  'datum': None,
  'datum_hash': None,
  'post_alonzo': False,
  'script': None,
}}]
```