"""
Sript définissant les fonctions utilitaires pour la base postgresql :
    - execute : executer une commande sans return
    - execute_file :executer un script
    - query : requête avec return
    
"""

import subprocess

from config import *
from .docker import exec


def execute(sql):

    exec(
        CONTAINER_NAME,
        "psql",
        "-U",
        DB_USER,
        "-d",
        DB_NAME,
        "-c",
        sql
    )


def execute_file(path):

    exec(
        CONTAINER_NAME,
        "psql",
        "-U",
        DB_USER,
        "-d",
        DB_NAME,
        "-f",
        path
    )


def query(sql):

    command = [

        "docker",
        "exec",
        "-i",

        CONTAINER_NAME,

        "psql",

        "-U",
        DB_USER,

        "-d",
        DB_NAME,

        "-A",

        "-F",
        "|",

        "-t",

        "-c",

        sql

    ]


    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )


    rows = []


    for line in result.stdout.splitlines():

        rows.append(
            line.split("|")
        )


    return rows