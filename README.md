# Mini ETL Synthea → OMOP CDM

> Projet pédagogique permettant de comprendre le modèle de données **OMOP Common Data Model (CDM)** et de construire un ETL simple en Python à partir des données générées par **Synthea**.

---

# Objectifs du projet

Il s'agit d'un projet d'apprentissage visant à comprendre :

- le modèle de données OMOP-CDM et ses concepts;
- le fonctionnement d'un ETL ;

---

# Architecture

```

                Synthea
                   │
                   ▼
				  ETL
                   │
                   ▼
          PostgreSQL OMOP
                   │
      ┌──────────────────────────┐
      ▼                          ▼
Exploration (EDA)       		SQL
                                 │
                                 ▼
                         Analyse clinique
```

Un installateur permet de charger automatiquement :

- Le modèle OMOP-CMP sur une base PostgreSQL
- De charger automatiquement les fichiers csv générés par Synthea dans ce modèle

---

# Utilisation

## prérequis :

- Synthea (Java 17 requis) à déposer dans installer/synthea :

```
git clone https://github.com/synthetichealth/synthea.git
cd synthea
./gradlew build check test
```

- Docker Desktop

- Python 3.12

```
pip install tqdm jupyter pandas sqlalchemy psycopg2-binary matplotlib
```

- les vocabulaires Athena (https://athena.ohdsi.org/vocabulary/list) à déposer dans installer/vocabulary : ICD10, LOINC et RxNorm

- me modèle de données OMOP-CDM (https://github.com/OHDSI/CommonDataModel) à déposer dans installer/CommonDataModel

---

## Créer le container Docker

ULe fichier docker-compose.yml est inclus dans ce dépôt. Pour créer le container :

```
docker compose up -d
docker ps
```

Cette commande doit retourner : 

```
CONTAINER ID   IMAGE          PORTS
xxxx           postgres:15    0.0.0.0:5432->5432
```

Pour vérifier si la création du container est conforme : 

```
docker exec -it database-postgres-1 bash
psql -U omop -d omop
SELECT version();
```

Pour quitter : \q puis exit

Pour se connecter directement à la base psql : 

```
docker exec -it database-postgres-1 psql -U omop -d omop
```

---

## Executer les scripts d'installation OMOP

Seules les tables suivantes sont exploitées pour garder le projet simple :

- person|
- visit_occurrence
- condition_occurrence
- drug_exposure
- measurement

pour créer le schéma OMOP + installer les fichiers de OMOP-CDM : 

```
python omop.py install
```

pour lancer le script de vérification de l'installation d'OMOP-CDM : 

```
python omop.py validate_omop
```

pour chercher une correspondance : 

```
python omop.py search E11.9
```

---

## Création des données Synthea

Une fois Synthea compilé dans installer/synthea :

```
./run_synthea -s 1784915154815 -p 100 --exporter.csv.export=true
```

Les fichiers Synthea sont créés dans /output/csv

Note : le temps de chargement de l'ETL peut être très long (plusieurs heures) en fonction du nombre de patients générés. Pour limiter la durée de chargement je n'ai créé que 100 patients.
Note : la seed 1784915154815 permet de suivre la même EDA disponible dans les notebooks Jupyter de ce projet.

---

## ETL Synthea -> OMOP

L'idée est de charger les fichiers générés par Synthea dans les tables OMOP :

- person ← patients.csv 
- visit_occurrence ← encounters.csv
- condition_occurrence ← conditions.csv
- drug_exposure ← medications.csv
- measurement ← observations.csv

commande pour initier l'ETL : 

```
python omop.py init-etl
```

commande pour valider l'ETL : 

```
python omop.py validate_synthea
```

Note : pour les drug si STOP est vide, on prend START comme date de fin.
Note : pour 100 patients il y a 75000 observations générées --> le script modules/reduce_observations.py permet de réduire ce volume à quelques observations par patients.

---

## Vider les tables automatiquement

La commande suivante permet de :

- vider les tables OMOP chargée
- vider les tables de mapping
- réinitialiser les séquences

```
python omop.py reset
```

---

# Gestion des identifiants

Les identifiants Synthea sont des UUID.

OMOP utilise des identifiants numériques.

Le projet crée donc une table de correspondance :

```
omop_etl.id_map
```

contenant :

| entity | source_id | omop_id |
|---------|-----------|---------|
| person | UUID | integer |
| visit | UUID | integer |
| condition | UUID | integer |
| drug | UUID | integer |
| measurement | UUID | integer |

Cette table permet de retrouver facilement les relations entre les différentes tables.

---

# Concepts OMOP

On utilise directement les concepts présents dans la table concept. Les recherches sont effectuées :

- par nom (`concept_name`)
- par code (`concept_code`)

Quelques mappings simples sont réalisés, par exemple pour les types de visites.

---

# Simplifications utilisées

Afin de garder un projet simple, plusieurs simplifications ont été retenues.

## Pas d'utilisation de l'ETL officiel OHDSI

Le projet ne dépend ainsi pas :

- d'ETL R
- d'ETL Java
- d'Usagi
- de WhiteRabbit
- d'Rabbit-In-A-Hat

L'objectif est de recréer un ETL simple pour comprendre son fonctionnement.

---

## Pas de mapping vers les concepts standards

Pour les tables suivantes :

- condition_occurrence
- drug_exposure
- measurement

les concepts sources sont directement utilisés comme concepts OMOP lorsque cela est possible.

Par exemple :

```
condition_concept_id = condition_source_concept_id
```

Cette simplification est acceptable pour découvrir OMOP mais ne respecte pas entièrement les recommandations de l'OHDSI.

Dans un ETL, les concepts devraient être convertis vers leurs concepts standards via les tables :

- concept_relationship
- concept_ancestor

---

## Mapping minimal

Les mappings implémentés concernent essentiellement :

- genre
- type de visite

Le reste est volontairement limité.

---

## Données ignorées

Certaines informations présentes dans Synthea ne sont pas importées :

- provider
- care_site
- payer
- observation
- device
- procedure
- immunization
- allergies
- claims

---

## Valeurs tronquées

Certaines colonnes OMOP sont limitées à 50 caractères.

Les valeurs textuelles trop longues sont automatiquement tronquées afin de respecter le modèle.

---

# Performances

Pour accélérer le chargement :

- préchargement des tables de mapping en mémoire ;
- utilisation de dictionnaires Python ;
- insertion par lot avec `pandas.to_sql()`;
- barre de progression (`tqdm`) pour les traitements longs.

---

# Limitations

Ce projet n'a pas vocation à produire une base OMOP conforme aux standards OHDSI.

Les principales limitations sont :

- absence de mapping complet vers les concepts standards ;
- absence de nombreuses tables OMOP ;
- règles métier simplifiées ;
- pas de gestion avancée des vocabulaires.
