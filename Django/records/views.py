import json
import datetime

from django.http import JsonResponse
from django.utils.dateparse import parse_date

from user.models import User
from food.models import Food
from .models import FoodRecord, UricacidRecord, FlareupRecord

# ----------------------------------------- Food Record -----------------------------------------

def addFoodRecord(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        openid = data.get('openid')
        food_name = data.get('food_name')
        quantity = data.get('quantity', 0)

        try:
            user = User.objects.get(openid=openid)
            food = Food.objects.get(name=food_name)
            food_record = FoodRecord.objects.create(
                user=user,
                food=food,
                quantity=quantity
            )
            return JsonResponse({'status': 'success', 'record_id': food_record.id})
        except (User.DoesNotExist, Food.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'User or Food not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def getFoodRecordsForDate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        openid = data.get('openid')
        date_str = data.get('date')  # expecting date in 'YYYY-MM-DD' format

        try:
            date = parse_date(date_str)
            if not date:
                raise ValueError("Invalid date format")

            start_of_day = datetime.datetime.combine(date, datetime.time.min)
            end_of_day = datetime.datetime.combine(date, datetime.time.max)

            user = User.objects.get(openid=openid)

            food_records = FoodRecord.objects.filter(
                user=user,
                created_at__range=(start_of_day, end_of_day)
            ).order_by('created_at')

            results = [
                {
                    'food_name': record.food.name,
                    'quantity': record.quantity,
                    'purine_content': record.quantity * record.food.purine_per_unit,
                    'created_at': record.created_at
                }
                for record in food_records
            ]

            return JsonResponse({'status': 'success', 'records': results})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# ----------------------------------------- Uric Acid Record -----------------------------------------

def addUricacidRecord(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        openid = data.get('openid')
        quantity = data.get('quantity', 0)

        try:
            user = User.objects.get(openid=openid)
            uricacid_record = UricacidRecord.objects.create(
                user=user,
                quantity=quantity
            )
            return JsonResponse({'status': 'success', 'record_id': uricacid_record.id})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# ----------------------------------------- Flareup Record -----------------------------------------

def addFlareupRecord(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        openid = data.get('openid')
        symptom = data.get('symptom')
        intense_level = data.get('intense_level')
        trigger = data.get('trigger')

        try:
            user = User.objects.get(openid=openid)
            flareup_record = FlareupRecord.objects.create(
                user=user,
                symptom=symptom,
                intense_level=intense_level,
                trigger=trigger
            )
            return JsonResponse({'status': 'success', 'record_id': flareup_record.id})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
