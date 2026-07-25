import pandas as pd

from sqlalchemy import create_engine

from tqdm import tqdm

from config import *
from modules.mapping import next_id, get_omop_id, get_all_mapping
from modules.concepts import get_concept_by_code


engine = create_engine(DB_URL)


def load_measurement():

    print("Chargement observations.csv")

    person_map = get_all_mapping("person")
    visit_map = get_all_mapping("visit")


    df = pd.read_csv(
        SYNTHEA / "observations.csv"
    )


    measurements = []


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



        measurement_id = next_id(
            "measurement"
        )



        # Synthea utilise généralement LOINC

        source_concept_id = get_concept_by_code(
            row["CODE"],
            "LOINC"
        )


        # Version simplifiée

        measurement_concept_id = source_concept_id



        value = row["VALUE"]


        value_as_number = None


        value_as_concept_id = 0



        # tentative de conversion numérique

        try:

            value_as_number = float(value)

        except:

            value_as_number = None



        start = pd.to_datetime(
            row["DATE"]
        )



        measurements.append({


            "measurement_id":
                measurement_id,


            "person_id":
                person_id,


            "measurement_concept_id":
                measurement_concept_id,


            "measurement_date":
                start.date(),


            "measurement_datetime":
                start,


            "measurement_time":
                None,


            "measurement_type_concept_id":
                32817,


            "operator_concept_id":
                0,


            "value_as_number":
                value_as_number,


            "value_as_concept_id":
                value_as_concept_id,


            "unit_concept_id":
                0,


            "range_low":
                None,


            "range_high":
                None,


            "provider_id":
                None,


            "visit_occurrence_id":
                visit_id,


            "visit_detail_id":
                None,


            "measurement_source_value":
                row["CODE"],


            "measurement_source_concept_id":
                source_concept_id,


            "unit_source_value":
                row["UNITS"],


            "value_source_value":
                str(value)

        })



    with engine.begin() as conn:


        pd.DataFrame(measurements).to_sql(

            "measurement",

            engine,

            schema="omop",

            if_exists="append",

            index=False

        )


    print(
        f"{len(measurements)} mesures importées."
    )