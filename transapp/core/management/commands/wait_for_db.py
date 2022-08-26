'''
Django command to wait for the database to be available.
'''
import time

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    '''Django command to wait for database.'''
    def handle(self, *args, **options):
        ''' '''
        while True:
            try:
                self.check(databases=['default'])
                self.stdout.write('DATABASE IS READY')
                break
            except:
                self.stdout.write('waiting for database...')
                time.sleep(1)