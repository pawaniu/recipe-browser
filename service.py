import pandas as pd
import math
from openpyxl import load_workbook

recipe_browser = './data/recipe-browser.xlsx'
def recipes_list():
    recipes = read_data(recipe_browser)
    return format_list(recipes)

def create_recipe(recipe):
    recipes = read_data(recipe_browser)
    id = recipes['id'].max() + 1
    if math.isnan(id):
        id = 1

    recipe['id'] = id
    df = pd.DataFrame([recipe])
    result = pd.concat([recipes, df], ignore_index=True)
    result.to_excel(recipe_browser, index=False)
    return format_list(df)


def format_list(df):
    df.reset_index(level=0, inplace=True)
    return df.to_json(orient='records')


def read_data(file_path):
    print("Reading data")
    return pd.read_excel(file_path)
