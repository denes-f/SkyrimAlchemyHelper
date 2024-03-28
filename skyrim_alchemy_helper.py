import csv


def main():
    effect_list = EffectList()
    with open('effects.csv', encoding='utf-8-sig') as effects_file:
        effects_reader = csv.reader(effects_file, delimiter=';')
        for row in effects_reader:
            effect = row[0]
            ingredient = row[1]
            effect_list.add_ingredient(ingredient, effect)
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
        queried_effect = effect_list.get_effect(query_ingredient, query_effect_order)
        queried_ingredients = effect_list.get_ingredients(queried_effect)
        print(f"\n{query_ingredient} effect {query_effect_order}: {queried_effect}")
        print("---------------------------------------------------")
        print(f"Ingredients: {', '.join(queried_ingredients)}\n\n")


class Ingredient:
    def __init__(self, name):
        self._name = name
        self._effects = []

    def add_effect(self, effect):
        self._effects.append(effect)

    @property
    def name(self):
        return self._name

    @property
    def effects(self):
        return self._effects


class EffectList:
    def __init__(self):
        self._ingredients = []

    def add_ingredient(self, ingredient_name, effect_name):
        for ingredient in self._ingredients:
            if ingredient.name == ingredient_name:
                ingredient.add_effect(effect_name)
                return
        ingredient = Ingredient(ingredient_name)
        ingredient.add_effect(effect_name)
        self._ingredients.append(ingredient)

    def get_effect(self, ingredient_name, effect_order):
        for ingredient in self._ingredients:
            if ingredient.name == ingredient_name:
                return ingredient.effects[effect_order - 1]

    def get_ingredients(self, effect_name):
        queried_ingredients = []
        for ingredient in self._ingredients:
            if effect_name in ingredient.effects:
                queried_ingredients.append(ingredient.name)
        queried_ingredients.sort()
        return queried_ingredients


if __name__ == '__main__':
    main()
