import argparse
import logging

from sigtech.api.datasets.ls import ls
from sigtech.api.datasets.rm import rm
from sigtech.api.datasets.upload import upload

logger = logging.getLogger("datasets")


def main():
    parser = argparse.ArgumentParser(description="Dataset CLI.")

    subparsers = parser.add_subparsers(dest="action")
    cp_parser = subparsers.add_parser("cp")
    cp_parser.add_argument("path", type=str),
    cp_parser.add_argument("dataset_id", type=str),
    cp_parser.add_argument(
        "-m", "--mode", default="append", type=str, choices=["append", "overwrite"]
    )

    ls_parser = subparsers.add_parser("ls")
    ls_parser.add_argument("identifier", type=str, nargs="?")

    rm_parser = subparsers.add_parser("rm")
    rm_parser.add_argument("identifier", type=str),
    rm_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.action == "cp":
        logger.info(
            f"Copying file {args.path} to dataset {args.dataset_id} mode={args.mode}"
        )
        upload(args.path, args.dataset_id, mode=args.mode)
    elif args.action == "ls":
        for identifier in ls(args.identifier):
            print(identifier)
    elif args.action == "rm":
        rm(args.identifier, dry_run=args.dry_run)
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
