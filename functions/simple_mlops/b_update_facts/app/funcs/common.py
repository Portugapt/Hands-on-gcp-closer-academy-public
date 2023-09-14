"""Common functions for the train_model pipeline."""
from pathlib import Path


def file_contents(path: Path) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().replace('\n', ' ')


def load_query(
    table_facts: str,
    table_raw: str,
    query_path: Path,
) -> str:
    '''Inserts raw data into a temporary table. Common pattern in our ETL pipelines.

    This function uses the function file_contents to call the appropriate
    SQL query and formats it with this function parameters.

    Args:
        table_facts (str): The fqn of the facts table in BigQuery.
        table_raw (str): The fqn of the raw table in BigQuery.
        query_path (Path): The path to the SQL query script.

    Returns:
        str: A string with the query built based on the args.
        This query can be executed later.
    '''
    query: str = file_contents(
        path=query_path
    ).format(
        table_source=table_raw,
        table_target=table_facts,
    )
    return query
