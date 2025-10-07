import subprocess
from pathlib import Path

from src.on_chain import vesting, bitwise
from opshin import builder


def main():
    script = Path(vesting.__file__).absolute()
    subprocess.run(f"uv run opshin build {script}".split())
    script = Path(bitwise.__file__).absolute()
    builder.build(script)
    subprocess.run(f"uv run opshin build {script}".split())


if __name__ == "__main__":
    main()
