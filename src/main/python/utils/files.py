#!/usr/bin/python3
# -*-coding:UTF-8 -*

import os

MAIN_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
def get_full_path(*path):
    return os.path.join(MAIN_DIRECTORY, *path)

# TODO Description de la fonction