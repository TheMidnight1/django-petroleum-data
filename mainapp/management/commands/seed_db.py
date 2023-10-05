import requests
from mainapp.models import PetroleumData
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Seed required data to database"

    def handle(self, *args, **options):
        if  PetroleumData.objects.count() == 0:
            print("seeding required data to the database..")
            try:
                response = requests.get("https://raw.githubusercontent.com/younginnovations/internship-challenges/master/programming/petroleum-report/data.json")
                response.raise_for_status()
                data = response.json()
                
                
                data_objects = []

                for item in data:
                    data_objects.append(
                        PetroleumData(
                            year=item["year"],
                            petroleum_product=item["petroleum_product"],
                            sale=item["sale"],
                            country=item["country"]
                        )
                    )

                PetroleumData.objects.bulk_create(data_objects)
                print(f"{len(data)} data were added to database.")
            
            except Exception as e:
                print(f"Something went wrong! {str(e)}")
        else:
            print("database already contains data.")
    
