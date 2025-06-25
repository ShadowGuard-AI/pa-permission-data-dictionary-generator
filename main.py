import argparse
import logging
import os
import json
from typing import Dict, List, Any
from pathspec import PathSpec
from rich.console import Console
from rich.table import Column, Table

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
PERMISSION_SYSTEMS = ["acl", "posix", "s3"] # Example permission systems


def setup_argparse() -> argparse.ArgumentParser:
    """Sets up the argument parser for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generates a data dictionary of permissions from various permission systems."
    )
    parser.add_argument(
        "--input-path",
        "-i",
        type=str,
        required=True,
        help="Path to the directory or file containing permission data.",
    )
    parser.add_argument(
        "--output-file",
        "-o",
        type=str,
        default="permission_data_dictionary.json",
        help="Path to the output JSON file.",
    )
    parser.add_argument(
        "--permission-system",
        "-s",
        type=str,
        choices=PERMISSION_SYSTEMS,
        required=True,
        help="The permission system to analyze (e.g., acl, posix, s3).",
    )
    parser.add_argument(
        "--include-patterns",
        "-I",
        type=str,
        nargs="*",
        help="Glob patterns to include specific files/directories.  Uses .gitignore syntax.",
    )
    parser.add_argument(
        "--exclude-patterns",
        "-E",
        type=str,
        nargs="*",
        help="Glob patterns to exclude specific files/directories. Uses .gitignore syntax.",
    )

    return parser


def load_permission_data(input_path: str, permission_system: str) -> List[Dict[str, Any]]:
    """
    Loads permission data from the specified input path, handling different permission systems.
    """
    logging.info(f"Loading permission data from {input_path} (system: {permission_system})")
    data: List[Dict[str, Any]] = []

    if os.path.isfile(input_path):
        try:
            with open(input_path, "r") as f:
                # Assuming the file contains a JSON array of permission entries.
                data = json.load(f)
        except FileNotFoundError as e:
            logging.error(f"Input file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from input file: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred while reading the input file: {e}")
            raise
    elif os.path.isdir(input_path):
        # Placeholder for directory scanning and permission extraction.
        # This is where permission extraction logic would go based on the `permission_system`.
        # For example, for POSIX: os.stat, os.access, etc.
        # For ACL: libraries like `acl` might be used.
        # For S3, boto3 would be used to retrieve bucket/object ACLs.
        logging.warning("Directory scanning not yet fully implemented.  Returning an empty list.")

    else:
        logging.error(f"Invalid input path: {input_path}. Must be a file or directory.")
        raise ValueError(f"Invalid input path: {input_path}")

    return data


def filter_permission_data(data: List[Dict[str, Any]], include_patterns: List[str] = None, exclude_patterns: List[str] = None) -> List[Dict[str, Any]]:
    """
    Filters permission data based on include and exclude patterns.
    """
    if not include_patterns and not exclude_patterns:
        return data  # No filtering needed

    include_spec = PathSpec.from_lines("gitwildmatch", include_patterns or [])
    exclude_spec = PathSpec.from_lines("gitwildmatch", exclude_patterns or [])

    filtered_data = []
    for item in data:
        resource_path = item.get("resource_path")  # Assuming each item has 'resource_path'
        if not resource_path:
            logging.warning(f"Skipping item: Missing 'resource_path': {item}")
            continue

        if include_patterns and not include_spec.match_file(resource_path):
            continue  # Skip if it doesn't match include patterns

        if exclude_patterns and exclude_spec.match_file(resource_path):
            continue  # Skip if it matches exclude patterns

        filtered_data.append(item)

    return filtered_data

def generate_data_dictionary(permission_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generates a data dictionary from the loaded permission data.
    This function assumes permission data has the format:
    [{"resource_path": "/path/to/resource", "permissions": {"read": True, "write": False, ...}}, ...]
    """
    data_dictionary: Dict[str, Any] = {}

    for item in permission_data:
        resource_path = item.get("resource_path")
        permissions = item.get("permissions")

        if not resource_path:
            logging.warning("Skipping entry: Missing resource_path")
            continue
        if not permissions:
             logging.warning(f"Skipping entry: Missing permissions for {resource_path}")
             continue

        data_dictionary[resource_path] = permissions

    return data_dictionary


def save_data_dictionary(data_dictionary: Dict[str, Any], output_file: str) -> None:
    """Saves the data dictionary to a JSON file."""
    try:
        with open(output_file, "w") as f:
            json.dump(data_dictionary, f, indent=4)
        logging.info(f"Data dictionary saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving data dictionary to file: {e}")
        raise

def print_data_dictionary(data_dictionary: Dict[str, Any]) -> None:
    """Prints the data dictionary to the console using Rich."""
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Resource Path", style="dim", width=60)
    table.add_column("Permissions", style="green")

    for resource_path, permissions in data_dictionary.items():
        table.add_row(resource_path, str(permissions))

    console.print(table)


def main() -> None:
    """Main function to orchestrate the permission data dictionary generation."""
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        # 1. Load the permission data
        permission_data = load_permission_data(args.input_path, args.permission_system)

        # 2. Filter the data based on include and exclude patterns.
        filtered_data = filter_permission_data(permission_data, args.include_patterns, args.exclude_patterns)

        # 3. Generate the data dictionary.
        data_dictionary = generate_data_dictionary(filtered_data)

        # 4. Save the data dictionary to a file.
        save_data_dictionary(data_dictionary, args.output_file)

        # 5. Print the data dictionary to the console.
        print_data_dictionary(data_dictionary)

    except ValueError as e:
        logging.error(f"Input error: {e}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Example Usage:
    # python main.py --input-path input.json --output-file output.json --permission-system acl --include-patterns "*.txt" --exclude-patterns "secret.txt"
    main()