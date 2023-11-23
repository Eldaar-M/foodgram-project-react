import datetime


def text_to_print(ingredients, recipes):
    ingredient = [
        (f"{index}. {ingredient['ingredient__name'].capitalize()} "
         f"- {ingredient['total']} "
         f"({ingredient['ingredient__measurement_unit']}).\n")
        for index, ingredient in enumerate(ingredients, 1)
    ]
    recipe = [f"{recipe}\n" for recipe in recipes]
    return "".join(
        (
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "Список покупок:\n",
            *ingredient,
            "\nРецепты:\n",
            *recipe
        )
    )
