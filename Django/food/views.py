import base64
import uuid
import json

from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.db.models import Q

from .models import Food

def searchFood(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        search_query = data.get('name', '')

        matching_foods = Food.objects.filter(Q(name__icontains=search_query))

        results = [
            {
                'name': food.name,
                'ms_unit': food.ms_unit,
                'purine_per_unit': food.purine_per_unit,
                'health_tip': food.health_tip,
                'image_url': food.image.url if food.image else None
            }
            for food in matching_foods
        ]

        return JsonResponse({'status': 'success', 'results': results})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def getFoodByName(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        food_name = data.get('name', '')

        try:
            food = Food.objects.get(name=food_name)

            food_details = {
                'name': food.name,
                'ms_unit': food.ms_unit,
                'purine_per_unit': food.purine_per_unit,
                'health_tip': food.health_tip,
                'image_url': food.image.url if food.image else None
            }

            return JsonResponse({'status': 'success', 'food': food_details})

        except Food.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Food not found', 'food_name': food_name})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})