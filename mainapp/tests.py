from django.test import TestCase

# mainapp/tests.py

from django.test import TestCase
from .models import PetroleumData

class PetroleumDataTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.data1 = PetroleumData.objects.create(
            year='2023',
            petroleum_product='Petrol',
            sale=1000,
            country='USA'
        )
        self.data2 = PetroleumData.objects.create(
            year='2023',
            petroleum_product='Diesel',
            sale=1500,
            country='Canada'
        )

    def test_petroleum_data_str(self):
        # Test the __str__ method of the PetroleumData model
        self.assertEqual(str(self.data1), '2023 - Petrol (USA)')
        self.assertEqual(str(self.data2), '2023 - Diesel (Canada)')

    def test_sales_total(self):
        # Test the total sales calculation for a specific year and product
        year = '2023'
        product = 'Petrol'
        total_sales = PetroleumData.total_sales(year, product)
        self.assertEqual(total_sales, 1000)

    def test_sales_average(self):
        # Test the average sales calculation for a specific product
        product = 'Petrol'
        average_sales = PetroleumData.average_sales(product)
        self.assertEqual(average_sales, 1000)

    def test_sales_by_country(self):
        # Test the total sales by country for a specific year and product
        year = '2023'
        product = 'Diesel'
        sales_by_country = PetroleumData.sales_by_country(year, product)
        self.assertEqual(sales_by_country['Canada'], 1500)
        self.assertEqual(sales_by_country.get('USA'), None)

    # Add more test cases as needed
