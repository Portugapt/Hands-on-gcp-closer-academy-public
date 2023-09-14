from pathlib import Path

from b_update_facts.app.funcs.common import file_contents, load_query


def test_file_contents(tmp_path: Path) -> None:
    # Create a temporary file with some text
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello, world!\nThis is a test file.")

    # Test that the file_contents function returns the correct contents
    assert file_contents(file_path) == "Hello, world! This is a test file."


def test_load_query(tmp_path: Path) -> None:
    # Create a temporary SQL query file with some text
    query_path = tmp_path / "test_query.sql"
    query_path.write_text(
        "SELECT * FROM {table_source} WHERE date > '2022-01-01';")

    # Test that the load_query function returns the correct query string
    table_facts = "my_project.my_dataset.my_facts_table"
    table_raw = "my_project.my_dataset.my_raw_table"
    expected_query = f"SELECT * FROM {table_raw} WHERE date > '2022-01-01';".format(
        table_source=table_raw,
        table_target=table_facts,
    )
    assert load_query(table_facts, table_raw, query_path) == expected_query
