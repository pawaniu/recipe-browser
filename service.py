import math
import datastoreApi
import read_file_gcs


def recipes_list():
    return datastoreApi.read_record()


def create_recipe(recipe):
    return datastoreApi.create_record(recipe)



