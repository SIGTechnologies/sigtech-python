import argparse
import logging

from sigtech.api.datasets import DatasetsApi
from sigtech.api.datasets.upload import upload

logger = logging.getLogger("datasets")


def ls(datasets_api, identifier=None):
    if identifier is None:
        logger.info("Listing all datasets")
        for dataset in datasets_api.datasets:
            yield dataset.id
        return
    elif "/" in identifier:
        dataset_id, pattern = identifier.split("/", maxsplit=1)
        if "*" in dataset_id:
            raise ValueError("Invalid specifier. Use `dataset/*` or `data*`")
        if pattern:
            logger.info(
                f"Listing files matching pattern: '{pattern}' in dataset: {dataset_id}"
            )
        else:
            logger.info(f"Listing all files in dataset {dataset_id}")
        for file in datasets_api.datasets[dataset_id].files.filter(pattern):
            yield f"{file.dataset_id}/{file.id}"
    elif "*" not in identifier:
        dataset_id = identifier
        logger.info(f"Listing all files in dataset: {dataset_id}")
        for file in datasets_api.datasets[dataset_id].files:
            yield f"{file.dataset_id}/{file.id}"
    else:
        dataset_id = identifier
        logger.info(f"Listing datasets matching pattern: '{dataset_id}'")
        for dataset in datasets_api.datasets.filter(dataset_id):
            yield dataset.id


def rm(datasets_api, identifier, dry_run=False):
    if "/" in identifier:
        dataset_id, pattern = identifier.split("/", maxsplit=1)
        if "*" in dataset_id:
            raise ValueError("Invalid specifier. Use `dataset/*` or `data*`")
        if pattern:
            logger.info(
                f"Removing files matching pattern: "
                f"'{pattern}' from dataset: {dataset_id}"
            )
        else:
            logger.info(f"Removing all files in dataset {dataset_id}")
        datasets_api.datasets[dataset_id].files.filter(pattern).delete(dry_run=dry_run)
    elif "*" not in identifier:
        dataset_id = identifier
        logger.info(f"Removing dataset {dataset_id}")
        datasets_api.datasets[dataset_id].delete()
    else:
        raise ValueError(
            "Invalid specifier. "
            "Use `dataset/*` to remove files or `dataset` to remove a dataset."
        )


def main():
    parser = argparse.ArgumentParser(description="Dataset CLI")

    subparsers = parser.add_subparsers(dest="action")
    cp_parser = subparsers.add_parser("cp")
    cp_parser.add_argument("path", type=str),
    cp_parser.add_argument("dataset_id", type=str),
    cp_parser.add_argument(
        "-m", "--mode", default="append", type=str, choices=["append", "overwrite"]
    )
    cp_parser.add_argument("-e", "--encoding", default="utf8", type=str)

    ls_parser = subparsers.add_parser("ls")
    ls_parser.add_argument("identifier", type=str, nargs="?")

    rm_parser = subparsers.add_parser("rm")
    rm_parser.add_argument("identifier", type=str),
    rm_parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    datasets_api = DatasetsApi()

    if args.action == "cp":
        logger.info(
            f"Copying file {args.path} to dataset {args.dataset_id} mode={args.mode}"
        )
        upload(args.path, args.dataset_id, mode=args.mode, encoding=args.encoding)
    elif args.action == "ls":
        for identifier in ls(datasets_api, args.identifier):
            print(identifier)
    elif args.action == "rm":
        rm(datasets_api, args.identifier, dry_run=args.dry_run)
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
