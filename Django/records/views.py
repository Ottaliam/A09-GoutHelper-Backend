import json

from django.http import JsonResponse

from user.models import User
from food.models import Food
from .models import FoodRecord, UricacidRecord, FlareupRecord

def addFoodRecord(request):
    if request.method == 'POST':
        openid = request.POST.get('openid')
        food_name = request.POST.get('food_name')
        quantity = request.POST.get('quantity', 0)

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

def addUricacidRecord(request):
    if request.method == 'POST':
        openid = request.POST.get('openid')
        quantity = request.POST.get('quantity', 0)

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

def addFlareupRecord(request):
    if request.method == 'POST':
        openid = request.POST.get('openid')
        symptom = request.POST.get('symptom')
        intense_level = request.POST.get('intense_level')
        trigger = request.POST.get('trigger')

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
