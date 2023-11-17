import datetime


def text_to_print(ingredients):
    return (
        (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
         f"Список покупок:\n"),
        "\n".join(
            [
                (f"{index}.{ingredient['ingredient__name']}  - "
                 f"{ingredient['total']}"
                 f"({ingredient['ingredient__measurement_unit']}).")
                for index, ingredient in enumerate(ingredients, 1)
            ]
        ),
        '\nПродукты для рецептов: ' + ", ".join(
            [f"{ingredient['recipe__name']}" for ingredient in ingredients]
        )
    )
