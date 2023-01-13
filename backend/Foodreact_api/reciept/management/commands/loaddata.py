import json
from pathlib import PurePath, Path
from csv import DictReader

from django.core.management.base import BaseCommand

from reciept.models import Ingredient


root = PurePath(__file__).parents[5]
data_roots = Path(root) / 'data'


class Command(BaseCommand):
    help = 'load ingredients'
    output_transaction = True

    def handle(self, *args, **options):
        for root in data_roots.iterdir():
            f = open(root, 'r', encoding='utf8')
            if root.suffix == '.csv':
                data = DictReader(
                    f,
                    fieldnames=['name', 'measurement_unit']
                )
            else:
                data = json.load(f)
            for row in data:
                ingredient = Ingredient.objects.create(**row)
                ingredient.save()
