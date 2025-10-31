import subprocess
import sys
from pathlib import Path

from src.on_chain import vesting
from opshin.builder import build as opshin_build, PlutusContract, DEFAULT_CONFIG
sys.setrecursionlimit(10000)


def main():
    script = Path(vesting.__file__).absolute()
    contract = opshin_build(script, config=DEFAULT_CONFIG.update(remove_trace=True))
    contract = PlutusContract(contract)
    contract.dump(Path(__file__).parent.parent.joinpath("build/vesting"))


if __name__ == "__main__":
    main()
