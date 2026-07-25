# Mini ETL Synthea → OMOP CDM (Python)

> Projet pédagogique permettant de comprendre le modèle de données **OMOP Common Data Model (CDM)** et de construire un ETL simple en Python à partir des données générées par **Synthea**.

---

# Objectifs du projet

L'objectif de ce projet n'est **pas** de remplacer les ETL officiels de l'OHDSI.

Il s'agit d'un projet d'apprentissage visant à comprendre :

- le modèle de données OMOP-CDM ;
- les principales tables cliniques ;
- le fonctionnement d'un ETL médical ;
- les concepts standards OMOP ;
- les problématiques d'identifiants entre systèmes.

L'ensemble du code a volontairement été gardé **simple**, sans framework ETL, afin de faciliter sa compréhension.

---

# Architecture

```
Synthea CSV
        │
        ▼
Python ETL
        │
        ▼
OMOP PostgreSQL
        │
        ▼
SQL / ATLAS / Python
```

Le projet importe directement les fichiers CSV produits par Synthea dans une base PostgreSQL contenant le modèle OMOP-CDM.

---

# Technologies

- Python 3.12
- PostgreSQL
- SQLAlchemy
- Pandas
- tqdm
- Synthea
- OMOP CDM v5.4

---

# Structure du projet

```
installer/

│
├── omop.py                 # Lance les différentes commandes
│
├── config.py
│
├── modules/
│   ├── concepts.py
│   ├── postgres.py
│   ├── mapping.py
│   ├── validation.py
│   ├── reset.py
│   │
│   └── etl/
│        ├── person.py
│        ├── visit.py
│        ├── condition.py
│        ├── drug.py
│        └── measurement.py
│
└── synthea/
     └── output/csv/
```

---

# Tables OMOP implémentées

Le projet importe actuellement les tables suivantes :

| Table | Statut |
|--------|--------|
| person | ✅ |
| visit_occurrence | ✅ |
| condition_occurrence | ✅ |
| drug_exposure | ✅ |
| measurement | ✅ |

Ces cinq tables suffisent déjà pour réaliser de nombreuses analyses exploratoires (EDA).

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

Le projet utilise directement les concepts présents dans la table :

```
concept
```

Les recherches sont effectuées :

- par nom (`concept_name`)
- par code (`concept_code`)

Quelques mappings simples sont réalisés, par exemple pour les types de visites.

---

# Simplifications utilisées

Afin de garder un projet simple, plusieurs simplifications ont été retenues.

## Pas d'utilisation de l'ETL officiel OHDSI

Le projet ne dépend pas :

- d'ETL R
- d'ETL Java
- d'Usagi
- de WhiteRabbit
- d'Rabbit-In-A-Hat

L'objectif est uniquement pédagogique.

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

Dans un ETL de production, les concepts devraient être convertis vers leurs concepts standards via les tables :

- concept_relationship
- concept_ancestor

---

## Mapping minimal

Les mappings implémentés concernent essentiellement :

- sexe
- type de visite

Le reste est volontairement limité.

---

## Données ignorées

Certaines informations présentes dans Synthea ne sont pas encore importées :

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

# Validation

Le projet possède un module de validation permettant de vérifier :

- les clés primaires
- les clés étrangères
- les concepts inexistants
- le nombre de lignes

Cette validation permet de détecter rapidement les erreurs de chargement.

---

# Reset

Une commande permet de remettre complètement la base à zéro.

Elle :

- vide les tables OMOP chargées ;
- vide les tables de mapping ;
- réinitialise les séquences.

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

---

# Cas d'usage

Ce projet est adapté pour :

- découvrir OMOP-CDM ;
- apprendre PostgreSQL ;
- comprendre un ETL médical ;
- réaliser des requêtes SQL ;
- effectuer de l'analyse exploratoire (EDA) ;
- préparer des projets de Data Science ou de Machine Learning sur des données de santé.

---

# Pistes d'amélioration

Les évolutions possibles sont nombreuses :

- mapping automatique vers les concepts standards ;
- import des procédures ;
- import des observations ;
- import des immunisations ;
- import des devices ;
- support des providers et care_sites ;
- chargement incrémental ;
- optimisation des performances ;
- génération de cohortes ;
- intégration avec ATLAS.

---

# Licence

Projet réalisé dans un objectif pédagogique.

Les données sont générées par **Synthea**, un générateur open source de dossiers patients synthétiques.

Le modèle de données utilisé est **OMOP Common Data Model (CDM)** développé par la communauté **OHDSI**.