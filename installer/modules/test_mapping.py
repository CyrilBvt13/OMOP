from modules.concepts import (
    get_concept_by_code,
    get_standard_concept,
    get_concept
)

def test_mapping():

    code = "E11.9"

    source = get_concept_by_code(code, "ICD10")
    print("Source ID :", source)
    print(get_concept(source))

    standard = get_standard_concept(source)
    print("Standard ID :", standard)
    print(get_concept(standard))