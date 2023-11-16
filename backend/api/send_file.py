import datetime


def sending(ingredients):
    count = 0
    text_to_print = (
        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Список покупок:\n"
    )
    for ingredient in ingredients:
        count += 1
        text_to_print += (
            f"{count}."
            f"{ingredient['ingredient__name']}  - "
            f"{ingredient['total']}"
            f"({ingredient['ingredient__measurement_unit']})."
            f" Рецепт:{ingredient['recipe__name']}\n"
        )
    return text_to_print
