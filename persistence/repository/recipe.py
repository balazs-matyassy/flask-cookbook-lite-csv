from persistence import get_path, get_delimiter
from persistence.model.recipe import Recipe


class RecipeRepository:
    @staticmethod
    def install():
        RecipeRepository.__store_all([])

    @staticmethod
    def find_all():
        with open(get_path('recipes.txt'), encoding='utf-8') as file:
            delimiter = get_delimiter()
            file.readline()  # header

            recipes = []

            for line in file:
                recipe = Recipe.create_from_line(line, delimiter)
                recipes.append(recipe)

            return recipes

    @staticmethod
    def find_by_id(recipe_id):
        for recipe in RecipeRepository.find_all():
            if recipe.recipe_id == recipe_id:
                return recipe

        return None

    @staticmethod
    def find_by_name(name):
        recipes = []

        for recipe in RecipeRepository.find_all():
            if name.lower() in recipe.name.lower():
                recipes.append(recipe)

        return recipes

    @staticmethod
    def save(recipe):
        recipes = RecipeRepository.find_all()

        if recipe.recipe_id is None:
            max_id = 0

            for i in range(len(recipes)):
                if recipes[i].recipe_id > max_id:
                    max_id = recipes[i].recipe_id

            recipe.recipe_id = max_id + 1
            recipes.append(recipe)
        else:
            for i in range(len(recipes)):
                if recipes[i].recipe_id == recipe.recipe_id:
                    recipes[i] = recipe
                    break

        RecipeRepository.__store_all(recipes)

        return recipe

    @staticmethod
    def delete_by_id(recipe_id):
        recipes = RecipeRepository.find_all()

        for i in range(len(recipes)):
            if recipes[i].recipe_id == recipe_id:
                recipes.pop(i)
                break

        RecipeRepository.__store_all(recipes)

    @staticmethod
    def __store_all(recipes):
        with open(get_path('recipes.txt'), 'w', encoding='utf-8') as file:
            delimiter = get_delimiter()

            file.write(
                f'id{delimiter}category{delimiter}name'
                f'{delimiter}description{delimiter}difficulty\n'
            )

            for recipe in sorted(recipes, key=lambda item: f'{item.category}\0{item.name}'):
                file.write(f'{recipe.to_line(delimiter)}\n')
