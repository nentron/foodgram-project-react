def create_ingredients_list(ingredients):
    ingredients_list = []
    for row in ingredients:
        line = '{0} ({1}) - {2}\n'.format(
            row.get('ingredient__name'),
            row.get('ingredient__measurement_unit'),
            row.get('amount_sum')
        )
        ingredients_list.append(line)
    return ingredients_list


if __name__ == '__main__':
    create_ingredients_list
