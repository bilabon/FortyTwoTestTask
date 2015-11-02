# -*- coding: utf-8 -*-

from StringIO import StringIO

from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.contenttypes.models import ContentType

from contact.tests.base import BaseSetup


class CommandTests(BaseSetup):
    '''
    Test infomodels command that prints all project models and
    the count of objects in every model.
    '''

    def test_command_infomodels_stdout(self):
        '''
        Testing stdout of command.
        '''
        stdout = StringIO()
        call_command('infomodels', stdout=stdout)
        for ct in ContentType.objects.all():
            m = ct.model_class()
            line = "%s.%s\t%d" % (
                m.__module__, m.__name__, m._default_manager.count())
            self.assertIn(line, stdout.getvalue())

    def test_command_infomodels_stderr(self):
        '''
        Testing stderr of command.
        '''
        stderr = StringIO()
        call_command('infomodels', stderr=stderr)
        for ct in ContentType.objects.all():
            m = ct.model_class()
            line = "%s.%s\t%d" % (
                m.__module__, m.__name__, m._default_manager.count())
            self.assertIn('Error: %s' % line, stderr.getvalue())

    def test_exeption_not_allow_any_args(self):
        '''
        Raise CommandError: The command does not allow any args
        '''
        self.assertRaises(CommandError, call_command, 'infomodels args')
