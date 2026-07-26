from modules.postgres import query
from config import SCHEMA


def get_concept_id(name, vocabulary):
    """
    Concept resolver : permet de trouver l'id d'un concept
    """

    sql = f"""

    SELECT concept_id

    FROM {SCHEMA}.concept

    WHERE concept_name='{name}'

    AND vocabulary_id='{vocabulary}'

    LIMIT 1;

    """

    result = query(sql)

    if result:
        return int(result[0][0])

    return 0



def get_visit_concept_id(encounter_class):

    mapping = {

        "ambulatory": 9202,      # Outpatient Visit
        "outpatient": 9202,

        "inpatient": 9201,       # Inpatient Visit

        "emergency": 9203,       # Emergency Room Visit

        "urgentcare": 9203,

        "wellness": 9202,

        "snf": 42898160,         # Skilled Nursing Facility

        "home": 581476,

    }

    return mapping.get(
        encounter_class.lower(),
        0
    )


def get_concept_by_code(code, vocabulary):
    """
    Recherche un concept OMOP à partir de son code source
    """

    sql = f"""

    SELECT concept_id

    FROM {SCHEMA}.concept

    WHERE concept_code='{code}'

    AND vocabulary_id='{vocabulary}'

    LIMIT 1;

    """

    result = query(sql)

    if result:
        return int(result[0][0])

    return 0


def get_standard_concept(source_concept_id):

    sql = f"""
    SELECT c2.concept_id

    FROM {SCHEMA}.concept_relationship cr

    JOIN {SCHEMA}.concept c2
        ON c2.concept_id = cr.concept_id_2

    WHERE cr.concept_id_1 = {source_concept_id}
      AND cr.relationship_id = 'Maps to'

    LIMIT 1;
    """

    result = query(sql)

    if result:
        return int(result[0][0])

    return 0


def get_concept(concept_id):

    sql = f"""
    SELECT concept_name,
           vocabulary_id,
           concept_code,
           standard_concept
    FROM {SCHEMA}.concept
    WHERE concept_id={concept_id};
    """

    result = query(sql)

    if result:
        return result[0]

    return None