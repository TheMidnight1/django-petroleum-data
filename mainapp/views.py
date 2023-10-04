import requests
from django.db.models import Sum
from .models import PetroleumData 
from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import Coalesce
from .serializers import PetroleumDataSerializer
from django.db.models import Avg, ExpressionWrapper, F, IntegerField

class PetroleumDataView(APIView):
    @transaction.atomic
    def get(self, request):
        url = "https://raw.githubusercontent.com/younginnovations/internship-challenges/master/programming/petroleum-report/data.json"

        try:
            response = requests.get(url)
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

            return Response({"message": "Data saved to the database."})
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=500)
        
class DisplayPetroleumDataView(APIView):
    def get(self, request):
        
        data = PetroleumData.objects.all()
        
        total_sales = PetroleumData.objects.values('petroleum_product').annotate(
        total_sale=Coalesce(Sum('sale'), 0)
        ).order_by('-total_sale')
        
        total_sales_by_country = PetroleumData.objects.values('country').annotate(
        total_sale=Coalesce(Sum('sale'), 0)
        ).order_by('-total_sale')

        top_countries = total_sales_by_country[:3]

        # bottom_countries = total_sales_by_country[len(total_sales_by_country) - 3:] 
        bottom_countries = total_sales_by_country[::-1][:3]
        
        avg_data = PetroleumData.objects.exclude(sale=0)

        # Calculate the average sale for each petroleum product over a 4-year interval
        average_sales = (
            avg_data.annotate(year_integer=ExpressionWrapper(
                F('year'), output_field=IntegerField()
            ))
            .annotate(year_mod=F('year_integer') % 4)
            .filter(year_mod=0)
            .values('petroleum_product', 'year_integer')
            .annotate(avg_sale=Avg('sale'))
            .order_by('petroleum_product', 'year_integer')
        )

        # Prepare the data for rendering in the desired format
        formatted_average_sales = []
        current_product = None
        start_year = None
        end_year = None
        total_sale = 0

        for item in average_sales:
            if item['petroleum_product'] != current_product:
                if current_product is not None:
                    formatted_average_sales.append({
                        'Product': current_product,
                        'Year': f'{start_year}-{end_year}',
                        'Avg': total_sale / (end_year - start_year + 1)
                    })
                current_product = item['petroleum_product']
                start_year = item['year_integer']
                end_year = item['year_integer']
                total_sale = item['avg_sale']
            else:
                end_year = item['year_integer']
                total_sale += item['avg_sale']

        # Add the last entry
        if current_product is not None:
            formatted_average_sales.append({
                'Product': current_product,
                'Year': f'{start_year}-{end_year}',
                'Avg': total_sale / (end_year - start_year + 1)
            })
        serializer = PetroleumDataSerializer(data, many=True)
        context = {"data": serializer.data , "total_sales":total_sales,"top_countries":top_countries, "bottom_countries":bottom_countries,"average_sales":formatted_average_sales}
        return render(request, "display_products.html", context)
    
    
