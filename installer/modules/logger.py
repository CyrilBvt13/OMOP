"""
Sript définissant les fonctions utilitaires pour l'affichage des logs dans l'invite de commande
"""

from colorama import Fore

def info(text):
    print(Fore.CYAN + "[INFO] " + text)

def ok(text):
    print(Fore.GREEN + "[ OK ] " + text)

def warning(text):
    print(Fore.YELLOW + "[WARN] " + text)

def error(text):
    print(Fore.RED + "[ERR ] " + text)