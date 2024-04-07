import csv
import sqlite3


def main():
    db_handler = DBHandler()
    while True:
        query_text = input("Search for an effect of an ingredient: ")
        query_split = query_text.rsplit(' ', 1)
        if len(query_split) != 2:
            print(f"Invalid input. Specify the query in the following format: Ingredient Name <space> Effect Order\n")
            continue
        query_ingredient = query_split[0]
        try:
            query_effect_order = int(query_split[1])
        except ValueError:
            print(f"Invalid Effect Order '{query_split[1]}'. The Effect Order should be a number\n")
            continue
        queried_effect = db_handler.get_effect(query_ingredient, query_effect_order)
        queried_ingredients = db_handler.get_ingredients(queried_effect)
        print(f"\n{query_ingredient} effect {query_effect_order}: {queried_effect}")
        print("---------------------------------------------------")
        print(f"Ingredients: {', '.join(queried_ingredients)}\n\n")


class DBHandler:
    def __init__(self):
        self._db_connection = sqlite3.connect("skyrim_alchemy.db")
        self._db_cursor = self._db_connection.cursor()

    def get_effect(self, ingredient_name, effect_order):
        res = self._db_cursor.execute('SELECT * FROM ingredients WHERE LOWER(Ingredient) IS ?', (ingredient_name.lower(),))
        effects = res.fetchone()
        effect = None if effects is None else effects[effect_order]
        return effect

    def get_ingredients(self, effect_name):
        res = self._db_cursor.execute('SELECT ingredient FROM ingredients WHERE ? IN ("primary_effect", "secondary_Effect", "tertiary_effect", "quaternary_effect")', (effect_name,))
        ingredients = [row[0] for row in res.fetchall()]
        ingredients.sort()
        return ingredients


if __name__ == '__main__':
    main()
