from django.core.management.base import BaseCommand

from users.utils import get_legal_date


class Command(BaseCommand):
    help = 'Extracts dates from given file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        print(path)
        with open(path) as f:
            for line in f:
                self.stdout.write(get_legal_date(line))

        self.stdout.write(self.style.SUCCESS('Successfully process file'))
