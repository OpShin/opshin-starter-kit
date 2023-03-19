from opshin import compiler
from pathlib import Path

from src.on_chain import vesting


def test_vesting_compile():
    path = Path(vesting.__file__).absolute()
    with open(path, "r") as f:
        source_code = f.read()
    source_ast = compiler.parse(source_code)
    code = compiler.compile(source_ast)
    print(code.dumps())
