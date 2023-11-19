import datetime


def text_to_print(ingredients, recipes_list):
    return (
        (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
         f"Список покупок:\n") + "\n".join(
            [
                (f"{index}. {ingredient['ingredient__name'].capitalize()} "
                 f"- {ingredient['total']}"
                 f"({ingredient['ingredient__measurement_unit']}).")
                for index, ingredient in enumerate(ingredients, 1)
            ]
        ) + "\nРецепты:\n" + "\n".join(
            set(
                [f"{recipe.recipe.name}" for recipe in recipes_list]
            )
        )
    )
