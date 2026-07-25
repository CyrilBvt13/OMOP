"""
Sript définissant les fonctions utilitaires pour l'installation de OMOP-CDM sur la base Postgresql
"""

from pathlib import Path

from config import *

from .postgres import (
    execute,
    execute_file
)

from .docker import copy

from .utils import prepare_sql

from .vocabulary import load_vocabulary


class Installer:


    def create_schema(self):

        print("\nCréation du schéma OMOP...")


        sql = f"""

DROP SCHEMA IF EXISTS {SCHEMA} CASCADE;


CREATE SCHEMA {SCHEMA};


"""


        execute(sql)


        print("✔ Schéma créé")



    def install_ddl(self):

        print("\nInstallation du DDL...")


        output = (
            SQL /
            "ddl.sql"
        )


        prepare_sql(
            DDL_SCRIPT,
            output,
            SCHEMA
        )


        copy(
            output,
            "/tmp/ddl.sql",
            CONTAINER_NAME
        )


        execute_file(
            "/tmp/ddl.sql"
        )


        print("✔ Tables OMOP créées")



    def install_primary_keys(self):

        print("\nInstallation des clés primaires...")


        output = (
            SQL /
            "primary_keys.sql"
        )


        prepare_sql(
            PRIMARY_KEYS,
            output,
            SCHEMA
        )


        copy(
            output,
            "/tmp/primary_keys.sql",
            CONTAINER_NAME
        )


        execute_file(
            "/tmp/primary_keys.sql"
        )


        print("✔ Primary keys installées")



    def install_vocabulary(self):

        load_vocabulary()



    def install_constraints(self):

        print("\nInstallation des contraintes...")


        output = (
            SQL /
            "constraints.sql"
        )


        prepare_sql(
            CONSTRAINTS,
            output,
            SCHEMA
        )


        copy(
            output,
            "/tmp/constraints.sql",
            CONTAINER_NAME
        )


        execute_file(
            "/tmp/constraints.sql"
        )


        print("✔ Contraintes installées")



    def install_indexes(self):

        print("\nInstallation des index...")


        output = (
            SQL /
            "indexes.sql"
        )


        prepare_sql(
            INDEXES,
            output,
            SCHEMA
        )


        copy(
            output,
            "/tmp/indexes.sql",
            CONTAINER_NAME
        )


        execute_file(
            "/tmp/indexes.sql"
        )


        print("✔ Index installés")