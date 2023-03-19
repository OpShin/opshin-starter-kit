# OpShin Starter-kit

This Starter-Kit is a small tutorial of how to use the [PyCardano](https://github.com/Python-Cardano/pycardano) library 
with [opshin](https://github.com/OpShin/opshin) for interacting with a simple vesting contract on Cardano.

PyCardano is a Cardano library written in Python. It allows users to create and sign transactions without depending on third-party Cardano serialization tools, such as cardano-cli and cardano-serialization-lib, making it a lightweight library, which is simple and fast to set up in all types of environments.

opshin is a Smart Contract language based on Python. It allows users to define and compile Smart Contracts directly within a python environment.
It also interacts seemlessly with PyCardano.

## Dev Environment

For executing the scripts in this starter kit you'll need access to a running [Ogmios](https://ogmios.dev/) instance.

In case you don't want to install the required components yourself, you can use [Demeter.run](https://demeter.run) platform to create a cloud environment with access to common Cardano infrastructure. The following command will open this repo in a private, web-based VSCode IDE with access to a running Ogmios instance in the preview network.

[![Code in Cardano Workspace](https://demeter.run/code/badge.svg)](https://demeter.run/code?repository=https://github.com/opshin/opshin-starter-kit&template=python)


## What is Included

We have included a number of python scripts for executing specific actions.
You can find scripts to initialize addresses and interact with the cardano-node in `scripts`.
`src` contains two folders, `on_chain` which hosts the actual opshin contract and `off-chain` which
hosts tooling to interact with the contract.


## Running the scripts


1. Install Python 3.8.
Installer [download](https://www.python.org/downloads/release/python-3810/)

2. Ensure `python3.8 --version` works in your command line.
In Windows, you can do this by copying the `python.exe` file to `python3.8.exe` in your `PATH` environment variable.

3. Install python poetry.
Follow the official documentation [here](https://python-poetry.org/docs/#installation).

4. Install a python virtual environment with poetry:
```bash
# install python dependencies
poetry install
# run a shell with the virtual environment activated
poetry shell
```

> TODO instruction on setting up Ogmios / cardano-node with demeter.run (or included in package?)

> TODO python3.8 and poetry and dependencies included in demeter.run?
