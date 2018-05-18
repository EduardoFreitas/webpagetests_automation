from dotenv import load_dotenv, find_dotenv
import os


def load_configuration():
    if not os.getenv("db_name"):
        load_dotenv(find_dotenv())