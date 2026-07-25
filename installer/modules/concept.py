from config import *
from .postgres import query



def get_concept(code):


    sql = f"""

SELECT

concept_id,
concept_name,
domain_id,
vocabulary_id,
concept_code

FROM {SCHEMA}.concept

WHERE concept_code='{code}';

"""


    result = query(sql)


    if not result:

        return None


    r = result[0]


    return {

        "id": r[0],
        "name": r[1],
        "domain": r[2],
        "vocabulary": r[3],
        "code": r[4]

    }

def get_mappings(concept_id):


    sql = f"""

SELECT

c.concept_id,
c.concept_name,
c.vocabulary_id,
c.concept_code

FROM {SCHEMA}.concept_relationship cr

JOIN {SCHEMA}.concept c

ON c.concept_id = cr.concept_id_2


WHERE

cr.concept_id_1={concept_id}

AND

cr.relationship_id='Maps to';

"""


    result = query(sql)


    concepts=[]


    for r in result:

        concepts.append({

            "id": r[0],
            "name": r[1],
            "vocabulary": r[2],
            "code": r[3]

        })


    return concepts