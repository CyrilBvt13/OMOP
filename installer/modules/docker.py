"""
Sript définissant les fonctions utilitaires pour la création du container Docker
"""

import subprocess

from .logger import info


def run(*args):

    command = [
        "docker",
        *args
    ]

    info(
        " ".join(command)
    )

    subprocess.run(
        command,
        check=True
    )


def exec(container, *args):

    run(
        "exec",
        "-i",
        container,
        *args
    )


def copy(source, destination, container):

    run(
        "cp",
        str(source),
        f"{container}:{destination}"
    )


def mkdir(path, container):

    exec(
        container,
        "mkdir",
        "-p",
        path
    )