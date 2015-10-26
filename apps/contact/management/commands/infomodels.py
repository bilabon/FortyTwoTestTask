from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    '''
    Django command that prints all project models and
    the count of objects in every model.
    Also:
        duplicate output to STDERR, prefixing each line with "error: "
        save output of STDERR into file logs/current_date.dat
    '''
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        if args:
            raise CommandError('Error: The command does not allow any args')

        for ct in ContentType.objects.all():
            m = ct.model_class()
            line = '%s.%s\t%d' % (
                m.__module__, m.__name__, m._default_manager.count())

            self.stdout.write(line)
            self.stderr.write('Error: %s' % (line))
