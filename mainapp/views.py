from django.db.models import Sum
from .models import PetroleumData 
from django.shortcuts import render
from rest_framework.views import APIView
from django.db.models.functions import Coalesce
from .serializers import PetroleumDataSerializer


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

        bottom_countries = total_sales_by_country[::-1][:3]

        # Filter the data for the year range 2007-2010 and calculate the average sale
        filtered_data_2007_2010 = [
            item for item in data
            if "2007" <= item.year <= "2010" and item.sale != 0
        ]

        result_2007_2010 = {}
        for item in filtered_data_2007_2010:
            key = f"{item.petroleum_product} - 2007-2010"
            if key not in result_2007_2010:
                result_2007_2010[key] = {
                    "Product": item.petroleum_product,
                    "Year": "2007-2010",
                    "Avg": item.sale,
                }
            else:
                result_2007_2010[key]["Avg"] += item.sale

        # Filter the data for the year range 2011-2014 and calculate the average sale
        filtered_data_2011_2014 = [
            item for item in data
            if "2011" <= item.year <= "2014" and item.sale != 0
        ]

        result_2011_2014 = {}
        for item in filtered_data_2011_2014:
            key = f"{item.petroleum_product} - 2011-2014"
            if key not in result_2011_2014:
                result_2011_2014[key] = {
                    "Product": item.petroleum_product,
                    "Year": "2011-2014",
                    "Avg": item.sale,
                }
            else:
                result_2011_2014[key]["Avg"] += item.sale

        # Combine the results for both year ranges
        average_sales = list(result_2007_2010.values()) + list(result_2011_2014.values())

        serializer = PetroleumDataSerializer(data, many=True)
        context = {"data": serializer.data , "total_sales":total_sales,"top_countries":top_countries, "bottom_countries":bottom_countries,"average_sales":average_sales}
        return render(request, "display_products.html", context)
    
    
