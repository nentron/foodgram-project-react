import json
import logging
import sys
from pathlib import PurePath, Path
from csv import DictReader

from django.core.management.base import BaseCommand

from reciept.models import Ingredient


LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(
    logging.Formatter(LOG_FORMAT)
)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


ROOT = PurePath(__file__).parents[5]
DATA_ROOTS = Path(ROOT) / 'data'


class Command(BaseCommand):
    help = 'Загрузка ингердиентов'

    def handle(self, *args, **options):
        for root in DATA_ROOTS.iterdir():
            logger.info(f'Загрузка файла {root.name}.')
            f = open(root, 'r', encoding='utf8')
            if root.suffix == '.csv':
                data = DictReader(
                    f,
                    fieldnames=['name', 'measurement_unit']
                )
            else:
                data = json.load(f)
            for row in data:
                Ingredient.objects.get_or_create(**row)
        logger.info('Загрузка завершенна.')
