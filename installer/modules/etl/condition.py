import pandas as pd

from sqlalchemy import create_engine

from tqdm import tqdm

from config import *

from modules.mapping import (
    next_id,
    add_mapping,
    get_omop_id,
    get_all_mapping,
    get_next_id
)

from modules.concepts import (
    get_concept_by_code
)

engine = create_engine(DB_URL)


def load_condition():

    person_map = get_all_mapping("person")
    visit_map = get_all_mapping("visit")

    df = pd.read_csv(
        SYNTHEA / "conditions.csv"
    )


    conditions = []


    mappings = []

    #for _, row in df.iterrows():
    for _, row in tqdm(
            df.iterrows(),
            total=len(df),
            desc="Chargement des conditions"
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
            continue



        # retrouver la visite OMOP

        #visit_id = get_omop_id(
        #    "visit",
        #    row["ENCOUNTER"]
        #)

        visit_id = visit_map.get(
            row["ENCOUNTER"]
        )



        # concept source

        source_concept_id = get_concept_by_code(
            row["CODE"],
            "ICD10CM"
        )

        # TODO :
        # Pour un ETL OMOP conforme, il faudra convertir le concept ICD10CM
        # vers son concept standard SNOMED ("Maps to").

        standard_concept_id = source_concept_id

        condition_id = next_id(
            "condition"
        )


        mappings.append({

            "entity": "condition",

            "source_id": condition_id,

            "omop_id": condition_id

        })



        conditions.append({

            "condition_occurrence_id":
                condition_id,


            "person_id":
                person_id,


            "condition_concept_id":
                standard_concept_id,


            "condition_start_date":
                pd.to_datetime(
                    row["START"]
                ).date(),


            "condition_start_datetime":
                pd.to_datetime(
                    row["START"]
                ),


            "condition_end_date":
                pd.to_datetime(
                    row["STOP"]
                ).date()
                if pd.notna(row["STOP"])
                else None,


            "condition_end_datetime":
                pd.to_datetime(
                    row["STOP"]
                )
                if pd.notna(row["STOP"])
                else None,


            "condition_type_concept_id":
                32817,


            "condition_source_concept_id":
                source_concept_id,


            "condition_source_value":
                row["CODE"],


            "visit_occurrence_id":
                visit_id

        })



    pd.DataFrame(conditions).to_sql(

        "condition_occurrence",

        engine,

        schema="omop",

        if_exists="append",

        index=False

    )


    print(
        len(conditions),
        "conditions importées"
    )