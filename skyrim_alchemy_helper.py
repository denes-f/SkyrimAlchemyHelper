import csv


def main():
    ingredient_list = IngredientList()
    with open('effects.csv', encoding='utf-8-sig') as effects_file:
        effects_reader = csv.reader(effects_file, delimiter=';')
        for row in effects_reader:
            effect = row[0]
            ingredient = row[1]
            ingredient_list.append(ingredient, effect)
    while True:
        query = input("Search for an effect of an ingredient: ")
        query_split = query.rsplit(' ', 1)
        query_ingredient = query_split[0]
        query_effect_order = int(query_split[1])
        queried_effect = ingredient_list.get_effect(query_ingredient, query_effect_order)
        queried_effect_ingredients = ingredient_list.get_ingredients(queried_effect)
        print(f"\n{query_ingredient} effect {query_effect_order}: {queried_effect}")
        print("---------------------------------------------------")
        print(f"Ingredients: {', '.join(queried_effect_ingredients)}\n\n")


class Ingredient:
    def __init__(self, name):
        self.name = name
        self.effects = []

    def add_effect(self, effect):
        self.effects.append(effect)

    def get_effects(self):
        return self.effects


class IngredientList:
    def __init__(self):
        self._ingredient_list = []

    def append(self, ingredient_name, effect_name):
        for ingredient in self._ingredient_list:
            if ingredient.name == ingredient_name:
                ingredient.add_effect(effect_name)
                return
        ingredient = Ingredient(ingredient_name)
        ingredient.add_effect(effect_name)
        self._ingredient_list.append(ingredient)

    def get_effect(self, ingredient_name, effect_order):
        for ingredient in self._ingredient_list:
            if ingredient.name == ingredient_name:
                return ingredient.effects[effect_order - 1]

    def get_ingredients(self, effect_name):
        filtered_ingredients = []
        for ingredient in self._ingredient_list:
            if effect_name in ingredient.effects:
                filtered_ingredients.append(ingredient.name)
        filtered_ingredients.sort()
        return filtered_ingredients


if __name__ == '__main__':
    main()
