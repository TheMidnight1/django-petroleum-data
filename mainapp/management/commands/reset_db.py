from mainapp.models import PetroleumData
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Delete data from database"

    def handle(self, *args, **options):
        print("reseting required data to the database..")
        data = PetroleumData.objects.all()
        total = len(data)
        data.delete()
        print(f"{total} data(s) were deleted successfully.")