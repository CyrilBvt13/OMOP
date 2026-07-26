Objectif : 

                Synthea
                   │
                   ▼
          (ETL officiel OHDSI)
                   │
                   ▼
          PostgreSQL OMOP
                   │
      ┌──────────────────────────┐
      ▼                          ▼
        Exploration (EDA)        SQL
                                 │
                                 ▼
                         Analyse clinique




prérequis :
- Synthea (Java 17 requis) --> A déposer dans installer/synthea

        git clone https://github.com/synthetichealth/synthea.git

        cd synthea

        ./gradlew build check test

- docker desktop

- python

        pip install tqdm jupyter pandas sqlalchemy psycopg2-binary matplotlib

- les vocabulaires Athena : https://athena.ohdsi.org/vocabulary/list --> A déposer dans installer/vocabulary

- le CDM : https://github.com/OHDSI/CommonDataModel --> A déposer dans installer/CommonDataModel




--- Créer le container docker :

Une fois le docker-compose.yml créé 

        docker compose up -d

        docker ps

doit retourner : 

        CONTAINER ID   IMAGE          PORTS
        xxxx           postgres:15    0.0.0.0:5432->5432

Pour vérifier : 

        docker exec -it database-postgres-1 bash

        psql -U omop -d omop

        SELECT version();

        quitter : \q

        puis : exit

Pour se connecter directement à la base psql : 

        docker exec -it database-postgres-1 psql -U omop -d omop



--- Executer les scripts d'installation OMOP

pour lancher le script d'installation : *

        python omop.py install

pour lancer le script de vérification : 

        python omop.py validate_omop

pour chercher une correspondance : 

        python omop.py search E11.9



---- Création des patients 

        ./run_synthea -p 100 --exporter.csv.export=true

les patients sont créés dans /output/csv

        Notes : le temps de chargement de l'ETL peut être très long (plusieurs heures) en fonction du nombre de patients générés.


---- ETL Synthea -> OMOP

L'idée est de charger les fichiers générés par Synthea dans les tables OMOP :
person ← patients.csv
visit_occurrence ← encounters.csv
condition_occurrence ← conditions.csv
drug_exposure ← medications.csv
measurement ← observations.csv

commande pour initier l'etl : 

        python omop.py init-etl

commande pour valider l'etl : 

        python omop.py validate_synthea

Notes : pour les drug si STOP est vide, on prend START comme date de fin.
Notes : pour 100 patients il y a 75000 observations générées --> le script modules/reduce_observations.py permet de réduire ce volume à quelques observations par patients.


---- Vider les tables automatiquement

        python omop.py reset


---- Exploration

------ EDA

------ Atlas