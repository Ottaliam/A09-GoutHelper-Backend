import os
import json
import datetime
import tempfile
import matplotlib.pyplot as plt
from collections import defaultdict

from django.http import JsonResponse
from django.utils.dateparse import parse_date

from user.models import User
from food.models import Food
from .models import FoodRecord, UricacidRecord, FlareupRecord
from django.conf import settings

# ---------------------------------------- Utils ----------------------------------------------
def generate_and_save_chart(data, title, temp_dir, date_format):
    plt.figure()
    dates = [date.strftime(date_format) for date in data.keys()]
    plt.plot(dates, data.values())
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Purine Intake')

    temp_file = tempfile.NamedTemporaryFile(dir=temp_dir, suffix='.png', delete=False)
    plt.savefig(temp_file.name)
    plt.close()

    return os.path.join(settings.MEDIA_URL, 'temp', os.path.basename(temp_file.name))

# ----------------------------------------- Food Record -----------------------------------------

def addFoodRecord(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        openid = data.get('openid')
        food_name = data.get('food_name')
        quantity = data.get('quantity', 0)
        record_date_str = data.get('record_date')

        try:
            record_date = datetime.datetime.strptime(record_date_str, '%Y-%m-%d').date()

            user = User.objects.get(openid=openid)
            food = Food.objects.get(name=food_name)
            food_record = FoodRecord.objects.create(
                user=user,
                food=food,
                quantity=quantity,
                record_date=record_date
            )
            return JsonResponse({'status': 'success', 'record_id': food_record.id})
        except (User.DoesNotExist, Food.DoesNotExist, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def computeStatisticsAndChartsForFoodRecord(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        record_date = datetime.datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Define time ranges based on given date
        last_7_days = [record_date - datetime.timedelta(days=i) for i in range(7)]
        last_month_end = record_date.replace(day=1) - datetime.timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        last_month = [last_month_start + datetime.timedelta(days=i) for i in range((last_month_end - last_month_start).days + 1)]
        last_year_start = record_date.replace(year=record_date.year-1, month=record_date.month+1, day=1)
        last_year = [last_year_start + datetime.timedelta(days=i) for i in range((record_date - last_year_start).days + 1)]

        # Fetch records and compute statistics
        statistics = {
            'last_7_days': defaultdict(float), 'last_month': defaultdict(float), 'last_year': defaultdict(float)
        }

        for date in last_7_days:
            records = FoodRecord.objects.filter(record_date=date)
            statistics['last_7_days'][date] += sum([r.quantity * r.food.purine_per_unit for r in records])

        for date in last_month:
            records = FoodRecord.objects.filter(record_date=date)
            statistics['last_month'][date] += sum([r.quantity * r.food.purine_per_unit for r in records])

        for month in range(1, 13):
            month_start = record_date.replace(month=month, day=1)
            month_end = (month_start + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
            records = FoodRecord.objects.filter(record_date__range=[month_start, month_end])
            month_key = month_start.strftime('%Y-%m')
            statistics['last_year'][month_key] += sum([r.quantity * r.food.purine_per_unit for r in records])

        # Generate and save charts
        charts = {
            'last_7_days_chart': generate_and_save_chart(statistics['last_7_days'], 'Purine Intake: Last 7 Days', temp_dir, '%m-%d'),
            'last_month_chart': generate_and_save_chart(statistics['last_month'], 'Purine Intake: Last Month', temp_dir, '%m-%d'),
            'last_year_chart': generate_and_save_chart(statistics['last_year'], 'Purine Intake: Last Year', temp_dir, '%Y-%m')
        }

        return JsonResponse({'status': 'success', 'charts': charts})
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
        record_date_str = data.get('record_date')

        try:
            record_date = datetime.datetime.strptime(record_date_str, '%Y-%m-%d').date()
            user = User.objects.get(openid=openid)
            uricacid_record = UricacidRecord.objects.create(
                user=user,
                quantity=quantity,
                record_date=record_date
            )
            return JsonResponse({'status': 'success', 'record_id': uricacid_record.id})
        except (User.DoesNotExist, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided'})
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
        record_date_str = data.get('record_date')

        try:
            record_date = datetime.datetime.strptime(record_date_str, '%Y-%m-%d').date()
            user = User.objects.get(openid=openid)
            flareup_record = FlareupRecord.objects.create(
                user=user,
                symptom=symptom,
                intense_level=intense_level,
                trigger=trigger,
                record_date=record_date
            )
            return JsonResponse({'status': 'success', 'record_id': flareup_record.id})
        except (User.DoesNotExist, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
