"""
Sript définissant la fonction permettant de vider les tables et schémas OMOP et OMOP-ETL
"""

from modules.postgres import execute


from modules.postgres import execute


def reset():

    print("==================================================")
    print("Reset complet de la base OMOP")
    print("==================================================")


    sql = """

    DO $$

    BEGIN

        IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema='omop_etl'
            AND table_name='measurement_mapping'
        )
        THEN
            TRUNCATE TABLE omop_etl.measurement_mapping;
        END IF;


        IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema='omop_etl'
            AND table_name='drug_mapping'
        )
        THEN
            TRUNCATE TABLE omop_etl.drug_mapping;
        END IF;


        IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema='omop_etl'
            AND table_name='condition_mapping'
        )
        THEN
            TRUNCATE TABLE omop_etl.condition_mapping;
        END IF;


        IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema='omop_etl'
            AND table_name='visit_mapping'
        )
        THEN
            TRUNCATE TABLE omop_etl.visit_mapping;
        END IF;


        IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema='omop_etl'
            AND table_name='person_mapping'
        )
        THEN
            TRUNCATE TABLE omop_etl.person_mapping;
        END IF;

        IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema='omop_etl'
            AND table_name='id_map'
        )
        THEN
            TRUNCATE TABLE omop_etl.id_map;
        END IF;


    END $$;


    TRUNCATE TABLE

        -- Tables OMOP
        omop.measurement,
        omop.drug_exposure,
        omop.condition_occurrence,
        omop.visit_occurrence,
        omop.person

    RESTART IDENTITY CASCADE;


    """


    execute(sql)


    print("")
    print("Reset terminé.")