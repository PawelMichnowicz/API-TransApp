from django.core.management.base import BaseCommand
import time 

class Command(BaseCommand):

    
    def handle(self, *args, **options):
        while True:
            try: 
                self.check(databases=['default'])
                self.stdout.write('DATABASE IS READY')
                break
            except:
                self.stdout.write('waiting for database...')
                time.sleep(1)