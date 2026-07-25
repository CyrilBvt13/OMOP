"""
Sript définissant les fonctions pour l'exploration des concepts OMOP
"""

from config import *

from .postgres import query

from .concept import (
    get_concept,
    get_mappings
)


def search(code):


    concept = get_concept(code)


    if concept is None:

        print(
            "Concept introuvable"
        )

        return



    print("""
====================================================
OMOP CONCEPT EXPLORER
====================================================
""")


    print("CONCEPT SOURCE")
    print("----------------")

    for k,v in concept.items():

        print(
            f"{k}: {v}"
        )



    mappings = get_mappings(
        concept["id"]
    )


    print("\nMAPS TO")
    print("----------------")


    if not mappings:

        print(
            "Aucun mapping"
        )


    for m in mappings:

        print()

        for k,v in m.items():

            print(
                f"{k}: {v}"
            )