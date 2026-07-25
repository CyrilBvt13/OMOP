import pandas as pd

from sqlalchemy import create_engine

from tqdm import tqdm

from config import *
from modules.mapping import next_id, get_omop_id, get_all_mapping
from modules.concepts import get_concept_by_code

engine = create_engine(DB_URL)


def load_drug():

    person_map = get_all_mapping("person")
    visit_map = get_all_mapping("visit")

    print("Chargement medications.csv")

    df = pd.read_csv(
        SYNTHEA / "medications.csv"
    )

    print(len(df), "lignes")

    drugs = []

    #for _, row in df.iterrows():
    for _, row in tqdm(
                df.iterrows(),
                total=len(df),
                desc="Chargement des prescriptions"
            ):

        #person_id = get_omop_id(
        #    "person",
        #    row["PATIENT"]
        #)

        person_id = person_map.get(
            row["PATIENT"]
        )

        if person_id is None:
            continue

        #visit_id = get_omop_id(
        #    "visit",
        #    row["ENCOUNTER"]
        #)

        visit_id = visit_map.get(
            row["ENCOUNTER"]
        )

        source_concept = get_concept_by_code(
            row["CODE"],
            "RxNorm"
        )

        standard_concept = source_concept

       # standard_concept = get_standard_concept(
       #     source_concept
       # )

        start = pd.to_datetime(
            row["START"]
        )

        end = None

        # OMOP impose une date de fin. Pour certaines lignes Synthea ne fournit pas STOP (traitement toujours actif?), on utilise provisoirement la date de début.
        if pd.isna(row["STOP"]):
            end = start
        else:
            end = pd.to_datetime(row["STOP"])

        drugs.append({

            "drug_exposure_id":
                next_id("drug"),

            "person_id":
                person_id,

            "drug_concept_id":
                standard_concept,

            "drug_exposure_start_date":
                start.date(),

            "drug_exposure_start_datetime":
                start,

            "drug_exposure_end_date":
                end.date() if end is not None else None,

            "drug_exposure_end_datetime":
                end,

            "verbatim_end_date":
                None,

            "drug_type_concept_id":
                32817,

            "stop_reason":
                None,

            "refills":
                row["DISPENSES"]
                if pd.notna(row["DISPENSES"])
                else None,

            "quantity":
                None,

            "days_supply":
                None,

            "sig":
                None,

            "route_concept_id":
                0,

            "lot_number":
                None,

            "provider_id":
                None,

            "visit_occurrence_id":
                visit_id,

            "visit_detail_id":
                None,

            "drug_source_value":
                row["CODE"],

            "drug_source_concept_id":
                source_concept,

            "route_source_value":
                None,

            "dose_unit_source_value":
                None

        })

    drug_df = pd.DataFrame(drugs)

    drug_df.to_sql(
        "drug_exposure",
        engine,
        schema="omop",
        if_exists="append",
        index=False,
        chunksize=1000
    )

    print()
    print(len(drug_df), "drug_exposure importés")