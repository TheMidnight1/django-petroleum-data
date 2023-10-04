from django.test import TestCase
from django.urls import reverse
from .models import PetroleumData

from rest_framework.test import APITestCase

class UrlTests(TestCase):
    def test_petroleum_data_url(self):
        response = self.client.get(reverse("mainapp:show"))
        self.assertEqual(response.status_code, 200) 

    def test_display_petroleum_data_url(self):
        response = self.client.get(reverse("mainapp:display-petroleum-data"))
        self.assertEqual(response.status_code, 200)  


class PetroleumDataModelTest(TestCase):
    def setUp(self):
        self.data = {
            "year": "2023",
            "petroleum_product": "Oil",
            "sale": 1000,
            "country": "USA"
        }

    def test_petroleum_data_model_creation(self):
        petroleum_data = PetroleumData(**self.data)
        petroleum_data.save()
        self.assertEqual(PetroleumData.objects.count(), 1)
        saved_data = PetroleumData.objects.get(year="2023")
        self.assertEqual(saved_data.petroleum_product, "Oil")
        self.assertEqual(saved_data.sale, 1000)
        self.assertEqual(saved_data.country, "USA")

class PetroleumDataViewTest(APITestCase):
    def test_petroleum_data_view(self):
        url = "https://raw.githubusercontent.com/younginnovations/internship-challenges/master/programming/petroleum-report/data.json"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "All data are shown"})
        self.assertEqual(PetroleumData.objects.count(), 0)
