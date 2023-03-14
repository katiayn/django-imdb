from django.core.management.base import BaseCommand

from catalogue.exceptions import TitleDoesNotExist
from catalogue.models import Title


IMDB_ID_LIST = [
    'tt2140553',
    'tt1796960',
    'tt2741602',
    'tt3205802',
    'tt1520211',
    'tt0773262',
    'tt1632701',
    'tt0108778',
    'tt0879870',
    'tt0230838',
    'tt3682448',
    'tt3170832',
    'tt2267998',
    'tt1895587',
    'tt0758758',
    'tt0268978',
    'tt0133093',
    'tt0289879',
    'tt1375666',
    'tt0109830',
    'tt4785654',
    'tt1754134',
    'tt9327842',
    'tt5753856',
    'tt2085059',
    'tt7366338',
    'tt2707408',
    'tt2356777',
    'tt0944947',
    'tt0903747',
    'tt0111161',
    'tt0317248',
    'tt6751668',
    'tt1475582',
    'tt0460649',
    'tt0203259',
    'tt0452046',
    'tt4574334',
    'tt2306299',
    'tt6468322',
    'tt2431438',
    'tt9642938',
    'tt11337908',
    'tt9698442',
]


class Command(BaseCommand):
    help = 'Add IMDb titles'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--imdb_ids', nargs='+', type=str, help='IMDb id (e.g. tt9698442')

    def handle(self, *args, **kwargs):
        imdb_ids = kwargs['imdb_ids'] or IMDB_ID_LIST

        for imdb_id in imdb_ids:
            try:
                exists, title = Title.get_or_create_title_by_imdb_id(imdb_id)
                if not exists:
                    self.stdout.write(self.style.SUCCESS(f'Title "{title.title}" was added successfully!'))
                else:
                    self.stdout.write(self.style.WARNING(f'Title "{title.title}" already exist in the database!'))
            except TitleDoesNotExist:
                self.stdout.write(self.style.ERROR(f'Title with imdb_id "{imdb_id}" does not exist.'))
