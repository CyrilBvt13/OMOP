from pathlib import Path


def prepare_sql(
    source,
    destination,
    schema
):

    content = Path(source).read_text(
        encoding="utf-8"
    )


    content = content.replace(
        "@cdmDatabaseSchema",
        schema
    )


    Path(destination).write_text(
        content,
        encoding="utf-8"
    )