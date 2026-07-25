"""
Sript définissant les fonctions pour le chargement des vocabulary (= terminologies de références) dans la base Postgresql
"""

from pathlib import Path

from config import *

from .docker import copy, mkdir
from .postgres import execute
from .logger import info, ok


VOCABULARY_FILES = [

    "VOCABULARY.csv",

    "DOMAIN.csv",

    "CONCEPT_CLASS.csv",

    "RELATIONSHIP.csv",

    "CONCEPT.csv",

    "CONCEPT_RELATIONSHIP.csv",

    "CONCEPT_SYNONYM.csv",

    "CONCEPT_ANCESTOR.csv",

    "DRUG_STRENGTH.csv"

]


def copy_vocabulary_files():

    info("Création du dossier vocabulaire dans le container")

    mkdir(
        CONTAINER_VOCABULARY,
        CONTAINER_NAME
    )


    info("Copie des vocabulaires")


    for file in VOCABULARY_FILES:

        source = VOCABULARY / file


        if not source.exists():

            info(
                f"{file} absent, ignoré"
            )

            continue


        copy(
            source,
            f"{CONTAINER_VOCABULARY}/{file}",
            CONTAINER_NAME
        )


        ok(file)

def load_vocabulary():


    copy_vocabulary_files()


    info(
        "Chargement des vocabulaires"
    )


    for file in VOCABULARY_FILES:


        table = file.replace(
            ".csv",
            ""
        ).lower()


        sql = f"""

COPY {SCHEMA}.{table}

FROM '{CONTAINER_VOCABULARY}/{file}'

WITH (

FORMAT csv,

DELIMITER E'\\t',

HEADER TRUE,

QUOTE E'\\b'

);

"""


        info(
            f"Import {table}"
        )


        execute(sql)


        ok(table)