"""
Sript définissant les commandes de la CLI OMOP

Liste des commandes disponibles :
    - install
    - validate_omop
    - search
    - init-etl
    - load_visit
    - validate_synthea
    - reset

"""

import argparse

from modules.installer import Installer

from modules.validator import validate_omop, validate_synthea

from modules.explorer import search

#from modules.synthea_loader import load_person

from modules.mapping import create_mapping_schema

from modules.etl.person import load_person
from modules.etl.visit import load_visit
from modules.etl.condition import load_condition
from modules.etl.drug import load_drug
from modules.etl.measurement import load_measurement
from modules.reduce_observations import reduce_observations

from modules.reset import reset

parser = argparse.ArgumentParser()


parser.add_argument(
    "command"
)

parser.add_argument(
    "value",
    nargs="?"
)


args = parser.parse_args()



installer = Installer()


# Commande pour créer le schéma OMOP + installer les fichiers de OMOP-CDM (OHDSI)
if args.command == "install":

    installer.create_schema()

    installer.install_ddl()

    installer.install_primary_keys()

    installer.install_vocabulary()

    installer.install_constraints()

    installer.install_indexes()


# Commande pour valider l'installation des fichiers OMOP-CDM
elif args.command == "validate_omop":

    validate_omop()


# Commande pour chercher un code
elif args.command == "search":

    search(args.value)


# Commande pour initier l'ETL à partir des fichiers générés par Synthea
elif args.command == "init-etl":

    create_mapping_schema()

    load_person()

    load_visit()

    load_condition()

    load_drug()

    reduce_observations()

    load_measurement()


# Commande pour charger les séjours uniquements
elif args.command == "load_measurement":

    reduce_observations()
    load_measurement()


# Commande pour valider l'init de l'ETL à partir des fichiers générés par Synthea
elif args.command == "validate_synthea":

    validate_synthea()


# Commande pour vider les tables et les schémas
elif args.command == "reset":

    reset()


else:

    print(
        "Commande inconnue"
    )