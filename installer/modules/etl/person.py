import pandas as pd

from sqlalchemy import create_engine
from tqdm import tqdm

from config import *

from modules.mapping import *

from modules.concepts import get_concept_id


engine = create_engine(DB_URL)


def load_person():

    df = pd.read_csv(
        SYNTHEA / "patients.csv"
    )

    male = get_concept_id(
        "Male",
        "SNOMED"
    )

    female = get_concept_id(
        "Female",
        "SNOMED"
    )

    persons = []

    mappings = []

    #for _, row in df.iterrows():
    for _, row in tqdm(
            df.iterrows(),
            total=len(df),
            desc="Chargement des patients"
        ):

        person_id = next_id("person")

        mappings.append({

            "entity": "person",

            "source_id": row["Id"],

            "omop_id": person_id

        })

        birth = pd.to_datetime(
            row["BIRTHDATE"]
        )

        persons.append({

            "person_id": person_id,

            "gender_concept_id":
                male if row["GENDER"] == "M"
                else female,

            "year_of_birth":
                birth.year,

            "month_of_birth":
                birth.month,

            "day_of_birth":
                birth.day,

            "birth_datetime":
                birth,

            "race_concept_id": 0,

            "ethnicity_concept_id": 0,

            "location_id": None,

            "provider_id": None,

            "care_site_id": None

        })

    pd.DataFrame(mappings).to_sql(

        "id_map",

        engine,

        schema="omop_etl",

        if_exists="append",

        index=False

    )

    pd.DataFrame(persons).to_sql(

        "person",

        engine,

        schema="omop",

        if_exists="append",

        index=False

    )

    print(f"{len(persons)} patients importés.")