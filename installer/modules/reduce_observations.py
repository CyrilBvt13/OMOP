import pandas as pd
import shutil

from config import SYNTHEA


MAX_OBSERVATIONS = 5


def reduce_observations():

    input_file = SYNTHEA / "observations.csv"
    output_file = SYNTHEA / "observations_reduced.csv"

    shutil.copy(
        SYNTHEA / "observations.csv",
        SYNTHEA / "observations_backup.csv"
    )
    
    print("Lecture de", input_file)

    df = pd.read_csv(input_file)

    print(len(df), "observations")

    # Trier pour ne garder que quelques observations par patients
    df = df.sort_values(["PATIENT", "CATEGORY", "DATE"])

    reduced = (
        df.groupby(
            ["PATIENT", "CATEGORY"],
            group_keys=False
        ).head(10)
    )

    reduced.to_csv(
        SYNTHEA / "observations.csv",
        index=False
    )

    print()
    print("Observations conservées :", len(reduced))
    print("Fichier créé :", output_file)


if __name__ == "__main__":
    reduce_observations()