"""
Fonctions utilitaires pour l'EDA
"""

from sqlalchemy import create_engine
import pandas as pd

DB_URL = (
    "postgresql+psycopg2://omop:omop"
    "@localhost:5432/omop"
)

#print(DB_URL)

engine = create_engine(DB_URL)


def sql(query):
    """
    Retourne un dataframe à partir d'une requête SQL
    """
    return pd.read_sql(query, engine)