import datetime


def text_to_print(ingredients, recipes):
    ingredient = [
        (f"{index}. {ingredient['ingredient__name'].capitalize()} "
         f"- {ingredient['total']} "
         f"({ingredient['ingredient__measurement_unit']}).")
        for index, ingredient in enumerate(ingredients, 1)
    ]
    recipe = [f"{recipe}" for recipe in recipes]
    return "\n".join(
        (
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "Список покупок:",
            *ingredient,
            "\nРецепты:",
            *recipe
        )
    )
