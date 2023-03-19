import subprocess
from pathlib import Path

from src.on_chain import vesting

def main():
    script = Path(vesting.__file__).absolute()
    subprocess.run(f"opshin build {script}".split())


if __name__ == "__main__":
    main()
