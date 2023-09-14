"""Common functions for the update_facts pipeline."""
import base64
from pathlib import Path


def get_path_to_file(path: str = './resources/select_train_data.sql') -> Path:
    return Path(path)


def file_contents(path: Path) -> str:
    """
    Reads the contents of a file and returns it as a string.

    Args:
        path (Path): The path to the file to be read.

    Returns:
        str: The contents of the file as a string.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', ' ')


def query_train_data(
    table_fqn: str,
    query_path: Path,
) -> str:
    '''Query to get training data from BigQuery.

    This function uses the function file_contents to call the appropriate
    SQL query and formats it with this function parameters.

    Args:
        table_fqn (str): The fully-qualified name of the table in BigQuery.
        query_path (Path): The path to the SQL query script.

    Returns:
        str: A string with the query built based on the args.
        This query can be executed later.
    '''
    query: str = file_contents(
        path=query_path
    ).format(
        table_source=table_fqn,
    )
    return query


def decode_base64_to_string(
    base64_string: str,
) -> str:
    '''Decodes a base64 string to a string.

    Args:
        base64_string (str): A base64 string.

    Returns:
        str: The decoded string.
    '''
    return base64.b64decode(base64_string).decode('utf-8')
