"""
Sript définissant :
    - la fonction permettant de valider le chargement de l'OMOP-CDM
    - la fonction permettant de valider le chargement de l'ETL Synthea
"""

from config import *

from .postgres import execute, query



# ------------------------------------------------------------------
# Validateur OMOP-CDM
# ------------------------------------------------------------------

OMOP_TABLES = [

    "person",

    "observation_period",

    "visit_occurrence",

    "condition_occurrence",

    "drug_exposure",

    "procedure_occurrence",

    "measurement",

    "observation",

    "death",

    "concept",

    "concept_relationship",

    "vocabulary",

]


def validate_schema():

    print("\nSchema")

    sql = f"""

SELECT EXISTS (

    SELECT 1

    FROM information_schema.schemata

    WHERE schema_name='{SCHEMA}'

);

"""

    execute(sql)



def validate_tables():

    print("\nTables")

    sql = f"""

SELECT COUNT(*)

FROM information_schema.tables

WHERE table_schema='{SCHEMA}';

"""

    execute(sql)



def validate_vocabulary():

    print("\nVocabulary")

    queries = {


        "Concepts":
        f"""
        SELECT COUNT(*)
        FROM {SCHEMA}.concept;
        """,


        "Relations":
        f"""
        SELECT COUNT(*)
        FROM {SCHEMA}.concept_relationship;
        """

    }


    for name, sql in queries.items():

        print(name)

        execute(sql)



def validate_constraints():

    print("\nConstraints")

    sql = """

SELECT COUNT(*)

FROM information_schema.table_constraints

WHERE constraint_type='FOREIGN KEY';

"""

    execute(sql)



def validate_indexes():

    print("\nIndexes")


    sql = f"""

SELECT COUNT(*)

FROM pg_indexes

WHERE schemaname='{SCHEMA}';

"""


    execute(sql)



def validate_omop():

    print(
        "\n=============================="
    )

    print(
        "OMOP VALIDATION"
    )

    print(
        "=============================="
    )


    validate_schema()

    validate_tables()

    validate_vocabulary()

    validate_constraints()

    validate_indexes()


    print(
        "\nValidation terminée"
    )




# ------------------------------------------------------------------
# Validateur ETL Synthea 
# ------------------------------------------------------------------

def print_title(title):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)



def check_count(table):

    sql = f"""
    SELECT COUNT(*)
    FROM omop.{table};
    """

    result = query(sql)

    count = result[0][0]

    print(
        f"{table:<30} {count:>10} lignes"
    )

    return count



def check_null(table, column):

    sql = f"""
    SELECT COUNT(*)

    FROM omop.{table}

    WHERE {column} IS NULL;
    """

    result = query(sql)

    count = result[0][0]

    status = "OK" if count == 0 else "ATTENTION"

    print(
        f"{table}.{column:<30} {status} ({count})"
    )



def check_fk(
    table,
    column,
    ref_table,
    ref_column
):

    sql = f"""

    SELECT COUNT(*)

    FROM omop.{table} t

    LEFT JOIN omop.{ref_table} r

    ON t.{column}=r.{ref_column}

    WHERE r.{ref_column} IS NULL;

    """

    result = query(sql)

    count = result[0][0]

    status = "OK" if count == 0 else "ERREUR"

    print(
        f"{table}.{column} -> {ref_table}.{ref_column} : {status} ({count})"
    )



def check_concept(table, column):

    sql = f"""

    SELECT COUNT(*)

    FROM omop.{table}

    WHERE {column}=0
    OR {column} IS NULL;

    """

    result = query(sql)

    count = result[0][0]

    status = "OK" if count == 0 else "ATTENTION"

    print(
        f"{table}.{column} concepts invalides : {status} ({count})"
    )



def validate_person():

    print_title("PERSON")

    check_count(
        "person"
    )

    check_null(
        "person",
        "person_id"
    )

    check_concept(
        "person",
        "gender_concept_id"
    )



def validate_visit():

    print_title("VISIT_OCCURRENCE")

    check_count(
        "visit_occurrence"
    )

    check_null(
        "visit_occurrence",
        "visit_occurrence_id"
    )

    check_fk(
        "visit_occurrence",
        "person_id",
        "person",
        "person_id"
    )

    check_concept(
        "visit_occurrence",
        "visit_concept_id"
    )



def validate_condition():

    print_title("CONDITION_OCCURRENCE")

    check_count(
        "condition_occurrence"
    )


    check_fk(
        "condition_occurrence",
        "person_id",
        "person",
        "person_id"
    )


    check_fk(
        "condition_occurrence",
        "visit_occurrence_id",
        "visit_occurrence",
        "visit_occurrence_id"
    )


    check_concept(
        "condition_occurrence",
        "condition_concept_id"
    )



def validate_drug():

    print_title("DRUG_EXPOSURE")

    check_count(
        "drug_exposure"
    )


    check_fk(
        "drug_exposure",
        "person_id",
        "person",
        "person_id"
    )


    check_fk(
        "drug_exposure",
        "visit_occurrence_id",
        "visit_occurrence",
        "visit_occurrence_id"
    )


    check_concept(
        "drug_exposure",
        "drug_concept_id"
    )



def validate_measurement():

    print_title("MEASUREMENT")

    check_count(
        "measurement"
    )


    check_fk(
        "measurement",
        "person_id",
        "person",
        "person_id"
    )


    check_fk(
        "measurement",
        "visit_occurrence_id",
        "visit_occurrence",
        "visit_occurrence_id"
    )


    check_concept(
        "measurement",
        "measurement_concept_id"
    )



def validate_synthea():

    print_title(
        "VALIDATION COMPLETE OMOP"
    )

    validate_person()

    validate_visit()

    validate_condition()

    validate_drug()

    validate_measurement()


    print("\nValidation terminée.")