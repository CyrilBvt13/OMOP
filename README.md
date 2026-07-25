Objectif : 

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
    Exploration (EDA)           SQL          
                                 │
                                 ▼
                         Analyse clinique




prérequis :
- Synthea (Java 17 requis) --> A placer dans installer/synthea

        git clone https://github.com/synthetichealth/synthea.git

        cd synthea

        ./gradlew build check test

- docker desktop

- python

        pip install tqdm

- les vocabulaires Athena : https://athena.ohdsi.org/vocabulary/list --> A placer dans installer/vocabulary

- le CDM : https://github.com/OHDSI/CommonDataModel --> A placer dans installer/CommonDataModel




--- Créer le container docker :

Une fois le docker-compose.yml créé 

    docker compose up -d

    docker ps

doit retourner : 

    CONTAINER ID   IMAGE          PORTS
    xxxx           postgres:15    0.0.0.0:5432->5432

Puis pour vérifier que tout est ok :

    docker exec -it database-postgres-1 bash

    psql -U omop -d omop

    SELECT version();

    quitter : \q

    puis : exit



--- Executer les scripts d'installation OMOP

pour lancher le script d'installation : python omop.py install

pour lancer le script de vérification : python omop.py validate_omop

pour chercher une correspondance : python omop.py search E11.9



---- Création des patients 

    ./run_synthea -p 100 --exporter.csv.export=true

les patients sont créés dans /output/csv



---- ETL Synthea -> OMOP

L'idée est de charger les fichiers générés par Synthea dans les tables OMOP simplifiées (on ne charge les 49 tables pour ce projet mais seulement les 5 plus importantes) :
person ← patients.csv
visit_occurrence ← encounters.csv
condition_occurrence ← conditions.csv
drug_exposure ← medications.csv
measurement ← observations.csv

commande pour initier l'etl : python omop.py init-etl

commande pour valider l'etl : python omop.py validate_synthea

Notes : pour les drug si STOP est vide, on prend START comme date de fin.


---- Vider les tables automatiquement

    python omop.py reset
