"""
Sript de configuration de l'installateur :
    - paramètres pour le container Docker
    - paramètres de la base Postgresql
    - répertoires du projet
    - scripts OMOP-CDM
    
"""

from pathlib import Path

# ------------------------------------------------------------------
# Docker
# ------------------------------------------------------------------

CONTAINER_NAME = "database-postgres-1"

# ------------------------------------------------------------------
# PostgreSQL
# ------------------------------------------------------------------

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "omop"
DB_USER = "omop"
DB_PASSWORD = "omop"

SCHEMA = "omop"

DB_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ------------------------------------------------------------------
# Répertoires
# ------------------------------------------------------------------

ROOT = Path(__file__).parent

COMMON_DATA_MODEL = ROOT / "CommonDataModel"

VOCABULARY = ROOT / "vocabulary"

SQL = ROOT / "sql"

LOGS = ROOT / "logs"

VOCABULARY = ROOT / "vocabulary"

CONTAINER_VOCABULARY = "/tmp/vocabulary"

SYNTHEA =  ROOT / "synthea" / "output" / "csv"

# ------------------------------------------------------------------
# Scripts OMOP
# ------------------------------------------------------------------

DDL = COMMON_DATA_MODEL / "inst/ddl/5.4/postgresql"

DDL_SCRIPT = DDL / "OMOPCDM_postgresql_5.4_ddl.sql"

PRIMARY_KEYS = DDL / "OMOPCDM_postgresql_5.4_primary_keys.sql"

CONSTRAINTS = DDL / "OMOPCDM_postgresql_5.4_constraints.sql"

INDEXES = DDL / "OMOPCDM_postgresql_5.4_indices.sql"