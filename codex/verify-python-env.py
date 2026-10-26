"""Check notebook dependencies without running or changing learner exercises."""

from importlib.metadata import version
from pathlib import Path
import sys

import ipykernel
from faker import Faker
from faker_commerce import Provider


def main() -> None:
    expected = Path(__file__).resolve().parent.parent / ".venv"
    if Path(sys.prefix).resolve() != expected.resolve() or sys.prefix == sys.base_prefix:
        raise SystemExit("Choose this checkout's .venv/Scripts/python.exe and try again.")
    if sys.version_info < (3, 11):
        raise SystemExit("Python 3.11 or newer is required.")
    fake = Faker()
    fake.add_provider(Provider)
    print(f"Interpreter: {sys.executable}")
    print(f"Python: {sys.version.split()[0]}")
    for package in ("ipykernel", "Faker", "faker-commerce"):
        print(f"{package}: {version(package)}")
    print("PASS: local environment, notebook kernel and Faker provider imports.")


if __name__ == "__main__":
    main()
