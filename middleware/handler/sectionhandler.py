from middleware.api.pokepedia import pokepedia_client
from middleware.db.repository import *
import middleware.processor.pokemonmoveprocessor as pokemonmoveprocessor
from middleware.util.helper import generationhelper
import logging
from dotenv import load_dotenv
import os

load_dotenv()


def handle_sections(page_file, level: int, after: str):
    file = open(page_file, "r")
    for line in file:
        sections = pokepedia_client.format_section_by_url(line)

    file.close()
