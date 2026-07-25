"""
Sript définissant les fonctions utilitaires pour le mapping OMOP
"""

from modules.postgres import execute, query

SCHEMA = "omop_etl"


def create_mapping_schema():
    """
    Crée le schéma et les tables techniques de l'ETL.
    """

    execute(f"""
        CREATE SCHEMA IF NOT EXISTS {SCHEMA};

        CREATE TABLE IF NOT EXISTS {SCHEMA}.id_map (
            entity      VARCHAR(50) NOT NULL,
            source_id   TEXT NOT NULL,
            omop_id     INTEGER NOT NULL,

            PRIMARY KEY(entity, source_id)
        );

        CREATE INDEX IF NOT EXISTS idx_id_map_lookup
            ON {SCHEMA}.id_map(entity, source_id);

        CREATE SEQUENCE IF NOT EXISTS {SCHEMA}.person_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS {SCHEMA}.visit_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS {SCHEMA}.condition_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS {SCHEMA}.drug_seq START 1;
        CREATE SEQUENCE IF NOT EXISTS {SCHEMA}.measurement_seq START 1;
    """)


def next_id(entity):
    """
    Retourne le prochain identifiant OMOP.
    """

    sequence = f"{SCHEMA}.{entity}_seq"

    return query(
        f"SELECT nextval('{sequence}')"
    )[0][0]


def add_mapping(entity, source_id, omop_id):
    """
    Ajoute un mapping entre un élement, sa source et son identifiant omop
    """

    execute(
        f"""
        INSERT INTO {SCHEMA}.id_map(entity, source_id, omop_id)
        VALUES('{entity}', '{source_id}', {omop_id})
        """
    )


def get_omop_id(entity, source_id):
    """
    Retourne l'identifiant omop d'un élement
    """

    result = query(
        f"""
        SELECT omop_id

        FROM {SCHEMA}.id_map

        WHERE entity='{entity}'

        AND source_id='{source_id}'
        """
    )

    if result:
        return result[0][0]

    return None


def get_all_mapping(entity):
    """
    Charge tous les mappings d'une entité en mémoire.
    """

    sql = f"""

    SELECT source_id, omop_id

    FROM {SCHEMA}.id_map

    WHERE entity='{entity}';

    """

    results = query(sql)

    return {
        row[0]: row[1]
        for row in results
    }


def get_next_id(entity):
    """
    Retourne le prochain ID disponible pour une entité OMOP.
    """

    sql = f"""

    SELECT COALESCE(MAX(omop_id), 0) + 1

    FROM omop_etl.id_map

    WHERE entity='{entity}';

    """

    result = query(sql)

    return int(result[0][0])