import pandas as pd
from tqdm import tqdm

from sqlalchemy import create_engine

from config import *

from modules.mapping import (
    next_id,
    add_mapping,
    get_omop_id,
    get_all_mapping
)

from modules.concepts import (
    get_visit_concept_id
)

engine = create_engine(DB_URL)



def load_visit():

    person_map = get_all_mapping("person")


    visits = pd.read_csv(
        SYNTHEA / "encounters.csv"
    )


    omop_visits = []


    mappings = []

    
    for _, row in tqdm(
        visits.iterrows(),
        total=len(visits),
        desc="Chargement des visites"
    ):


        # retrouver le patient OMOP

        #person_id = get_omop_id(
        #    "person",
        #    row["PATIENT"]
        #)
        
        person_id = person_map.get(
            row["PATIENT"]
        )


        if person_id is None:
            print(
                "Patient inconnu :",
                row["PATIENT"]
            )
            continue


        visit_id = next_id(
            "visit"
        )


        mappings.append({

            "entity": "visit",

            "source_id": row["Id"],

            "omop_id": visit_id

        })


        omop_visits.append({


            "visit_occurrence_id":
                visit_id,


            "person_id":
                person_id,


            "visit_concept_id":
                get_visit_concept_id(
                    row["ENCOUNTERCLASS"]
                ),


            "visit_start_date":
                pd.to_datetime(
                    row["START"]
                ).date(),


            "visit_start_datetime":
                pd.to_datetime(
                    row["START"]
                ),


            "visit_end_date":
                pd.to_datetime(
                    row["STOP"]
                ).date(),


            "visit_end_datetime":
                pd.to_datetime(
                    row["STOP"]
                ),


            "visit_type_concept_id":
                32817,


            "provider_id":
                None,


            "care_site_id":
                None,


            "visit_source_value":
                row["ENCOUNTERCLASS"],


            "visit_source_concept_id":
                0

        })


    # insertion mapping

    pd.DataFrame(mappings).to_sql(

        "id_map",

        engine,

        schema="omop_etl",

        if_exists="append",

        index=False

    )


    # insertion OMOP

    pd.DataFrame(omop_visits).to_sql(

        "visit_occurrence",

        engine,

        schema="omop",

        if_exists="append",

        index=False

    )


    print(
        len(omop_visits),
        "visites importées"
    )