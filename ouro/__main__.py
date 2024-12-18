import argparse
import json
from pathlib import Path
from time import time

from ouro import __version__
from ouro.checker import Checker
from ouro.utils import logger


def parse():
    parser = argparse.ArgumentParser(
        prog="ouro",
        description=(
            "ouro is a Python package that checks "
            + "your code for circular (cyclic) imports."
        ),
    )

    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        default=Path.cwd(),
        help=(
            "path to the Python project to be checked "
            + "(default: current working directory)"
        ),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"ouro {__version__}",
        help="show version number and exit",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="increase output verbosity (print report to console)",
    )
    parser.add_argument(
        "-t",
        "--strict",
        action="store_true",
        help=(
            "analyse internal function imports "
            + "(normally skipped because they cause no errors)"
        ),
    )
    parser.add_argument(
        "--no-categorize",
        action="store_true",
        help="don't categorize cycles (mark all cycles as critical)",
    )
    parser.add_argument(
        "-e",
        "--export",
        action="store_true",
        help="export the report to a json file",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        type=str,
        nargs="+",
        help="list of files, directories, or glob patterns to ignore",
    )

    return parser.parse_args()


def main():
    args = parse()
    start_time = time()

    logger.info("OURO IS STARTING...", highlight=True)
    logger.info("SCANNING FILES...", highlight=True)

    logger.info("OPTIONS:", highlight=True)
    logger.info(f" ==> PATH       : {args.path}")
    logger.info(f" ==> EXPORT     : {args.export}")
    logger.info(f" ==> VERBOSE    : {args.verbose}")
    logger.info(f" ==> STRICT     : {args.strict}")
    logger.info(f" ==> IGNORING   : {args.ignore}")
    logger.info(f" ==> CATEGORIZE : {not args.no_categorize}")

    checker = Checker(
        path=args.path,
        strict=args.strict,
        ignore=args.ignore,
        categorize=(not args.no_categorize),
    )
    if cycles := checker.cycles:
        retv = 1
        possible_origins = checker.get_possible_origins(cycles)

        logger.fail("FOUND CIRCULAR IMPORT(S)!", highlight=True)
        logger.warn("PROBABLY ONE OF THE FOLLOWING IS THE ORIGIN", highlight=True)

        for possible_origin in possible_origins:
            logger.warn(f" ==> {possible_origin}")

        if args.verbose:
            logger.info("PRINTING REPORT TO CONSOLE")
            print(json.dumps(cycles, indent=4))

        if args.export:
            export_path = Path.cwd() / "ouro-report.json"

            with open("ouro-report.json", "w") as output_file:
                logger.info(f"EXPORTING REPORT TO: {export_path}", highlight=True)
                json.dump(cycles, output_file, indent=4)

            logger.success(f"REPORT EXPORTED TO: {export_path}", highlight=True)
    else:
        retv = 0

        logger.success("WHOA! NO CIRCULAR IMPORT(S) FOUND!", highlight=True)

    logger.info(f"ELAPSED TIME: {time() - start_time:.2f} seconds", highlight=True)

    return retv


if __name__ == "__main__":
    raise SystemExit(main())
