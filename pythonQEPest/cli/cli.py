from __future__ import annotations

import argparse
import logging
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from collections.abc import Sequence

from pythonQEPest.dto import QEPestFile
from pythonQEPest.services.QEPestFileService import QEPestFileService

logger = logging.getLogger(__name__)


def _resolve_package_version() -> str:
    try:
        return version("pythonQEPest")
    except PackageNotFoundError:
        pass

    try:
        import tomllib  # py3.11+

        pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        return data["project"]["version"]
    except Exception:
        return "0+unknown"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pythonqepest",
        description="Compute QEPest scores from a tab-separated input file.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {_resolve_package_version()}",
        help="Show program's version number.",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="data.txt",
        help="Path to input tab-separated file with "
        + "QEPest descriptors (default: data.txt).",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="data.out.txt",
        help="Path to output tab-separated file with "
        + "QEPest descriptors (default: data.txt.out).",
    )

    parser.add_argument(
        "-f",
        "--format",
        default="txt",
        help="Format to output file with QEPest (json, txt).",
    )

    parser.add_argument(
        "--smiles",
        action="store_true",
        help="Input file contains SMILES strings "
        "(one per line) instead of descriptors.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    from dotenv import load_dotenv

    from pythonQEPest.core.qepest import QEPest
    from pythonQEPest.logger import init_logger

    args = build_parser().parse_args(argv)

    load_dotenv()
    init_logger()

    logger.debug("CLI initiated")
    logger.info(f"CLI args: {argv}")

    service = QEPestFileService(
        qepest=QEPest(),
        qepest_file=QEPestFile(
            input_file=args.input,
            output_file=args.output,
            format=args.format,
            smiles=args.smiles,
        ),
    )

    service.read_file_and_compute_params()

    return 0 if not service.error else 1
