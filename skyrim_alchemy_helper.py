import sqlite3


def main():
    db_handler = DBHandler()
    print("---------------------")
    print("Skyrim Alchemy Helper")
    print("---------------------\n")
    while True:
        query_text = input("Search for an effect of an ingredient: ")
        query_split = query_text.rsplit(' ', 1)
        if len(query_split) != 2:
            print(f"Invalid input. Specify the query in the following format: IngredientName <space> EffectOrder\n")
            continue
        query_ingredient = query_split[0]
        if query_split[1].lower() == 'a':
            query_effect_order = [1, 2, 3, 4]
        else:
            try:
                query_effect_order = [int(query_split[1])]
                if query_effect_order[0] not in [1, 2, 3, 4]:
                    print(f"Invalid Effect Order '{query_effect_order[0]}'\n")
                    continue
            except ValueError:
                print(f"Invalid Effect Order '{query_split[1]}'. "
                      f"The Effect Order should be a number or 'a' for displaying all effects\n")
                continue
        for effect_order in query_effect_order:
            queried_effect = db_handler.get_effect(query_ingredient, effect_order)
            queried_ingredients = db_handler.get_ingredients(queried_effect)
            result_title = f"{query_ingredient.title()} effect {effect_order}: {queried_effect}"
            print("-" * len(result_title))
            print(result_title)
            print("-" * len(result_title))
            print(f"Ingredients: {', '.join(queried_ingredients)}\n")
        print("\n")


class DBHandler:
    def __init__(self):
        self._connection = sqlite3.connect("skyrim_alchemy.db")
        self._cursor = self._connection.cursor()

    def get_effect(self, ingredient_name, effect_order):
        result = self._cursor.execute('SELECT * FROM ingredients WHERE LOWER(Ingredient) IS ?',
                                      (ingredient_name.lower(),))
        effects = result.fetchone()
        effect = None if effects is None else effects[effect_order]
        return effect

    def get_ingredients(self, effect_name):
        result = self._cursor.execute('SELECT ingredient FROM ingredients WHERE ? IN '
                                      '("primary_effect", "secondary_Effect", "tertiary_effect", "quaternary_effect")',
                                      (effect_name,))
        ingredients = [row[0] for row in result.fetchall()]
        ingredients.sort()
        return ingredients


if __name__ == '__main__':
    main()
