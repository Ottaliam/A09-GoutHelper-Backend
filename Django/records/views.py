import os
import io
import base64
import json
import datetime
from datetime import timedelta
import tempfile
import matplotlib.pyplot as plt

from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.db.models import Sum, Avg, F, functions

from user.models import User
from food.models import Food
from .models import FoodRecord, UricacidRecord, FlareupRecord
from django.conf import settings


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

def getFoodRecordSummary(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reference_date_str = data.get('reference_date')
        openid = data.get('openid')

        reference_date = datetime.datetime.strptime(reference_date_str, '%Y-%m-%d').date()
            
        # Helper function to compute start dates
        def start_date_for_period(days):
            return reference_date - datetime.timedelta(days=days)

        # Helper function to fill in missing dates with 0
        def fill_missing_dates(data, start_date, end_date, date_trunc):
            filled_data = {}
            current_date = start_date
            while current_date <= end_date:
                key = current_date.strftime('%Y-%m-%d') if date_trunc == 'day' else current_date.strftime('%Y-%m')
                filled_data[key] = 0
                current_date += datetime.timedelta(days=1 if date_trunc == 'day' else 30)

            for item in data:
                key = item['period'].strftime('%Y-%m-%d') if date_trunc == 'day' else item['period'].strftime('%Y-%m')
                filled_data[key] = item['total_purine']

            return [{'period': key, 'total_purine': value} for key, value in filled_data.items()]

        # Get the starting dates for each period
        last_week_start = start_date_for_period(7)
        last_month_start = start_date_for_period(30)
        last_year_start = start_date_for_period(365)

        # Helper function to annotate and aggregate query
        def aggregate_purine(queryset, date_trunc='day'):
            if date_trunc == 'day':
                trunc_date = functions.TruncDay('record_date')
            elif date_trunc == 'month':
                trunc_date = functions.TruncMonth('record_date')

            return queryset.annotate(
                period=trunc_date
            ).values('period').annotate(
                total_purine=Sum(F('quantity') * F('food__purine_per_unit'))
            ).order_by('period')

        # Query for each time period
        user = User.objects.filter(openid=openid).first()
        if not user:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        
        last_week_data = FoodRecord.objects.filter(
            user=user,
            record_date__range=[last_week_start, reference_date]
        )
        last_month_data = FoodRecord.objects.filter(
            user=user,
            record_date__range=[last_month_start, reference_date]
        )
        last_year_data = FoodRecord.objects.filter(
            user=user,
            record_date__range=[last_year_start, reference_date]
        )

        # Aggregate data
        weekly_purine = aggregate_purine(last_week_data, 'day')
        monthly_purine = aggregate_purine(last_month_data, 'day')
        yearly_purine = aggregate_purine(last_year_data, 'month')

        # Fill in missing dates
        filled_weekly_purine = fill_missing_dates(weekly_purine, last_week_start, reference_date, 'day')
        filled_monthly_purine = fill_missing_dates(monthly_purine, last_month_start, reference_date, 'day')
        filled_yearly_purine = fill_missing_dates(yearly_purine, last_year_start, reference_date, 'month')

        summary = {
            'last_week': filled_weekly_purine,
            'last_month': filled_monthly_purine,
            'last_year': filled_yearly_purine
        }

        return JsonResponse({'status': 'success', 'summary': summary})
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

            user = User.objects.get(openid=openid)

            food_records = FoodRecord.objects.filter(
                user=user,
                record_date=date
            ).order_by('created_at')

            results = [
                {
                    'food_name': record.food.name,
                    'ms_unit': record.food.ms_unit,
                    'image_url': record.food.image.url if record.food.image else None,
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

def getUricacidSummary(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reference_date_str = data.get('reference_date')
        openid = data.get('openid')

        reference_date = datetime.datetime.strptime(reference_date_str, '%Y-%m-%d').date()
    
        # Helper function to compute start dates
        def start_date_for_period(days):
            return reference_date - datetime.timedelta(days=days)

        # Helper function to fill in missing dates with 0
        def fill_missing_dates(data, start_date, end_date, date_trunc):
            filled_data = {}
            current_date = start_date
            while current_date <= end_date:
                key = current_date.strftime('%Y-%m-%d') if date_trunc == 'day' else current_date.strftime('%Y-%m')
                filled_data[key] = 0
                current_date += datetime.timedelta(days=1 if date_trunc == 'day' else 30)

            for item in data:
                key = item['period'].strftime('%Y-%m-%d') if date_trunc == 'day' else item['period'].strftime('%Y-%m')
                filled_data[key] = item['average_quantity']

            return [{'period': key, 'average_quantity': value} for key, value in filled_data.items()]

        # Get the starting dates for each period
        last_week_start = start_date_for_period(7)
        last_month_start = start_date_for_period(30)
        last_year_start = start_date_for_period(365)

        # Aggregate average
        def aggregate_uricacid(queryset, date_trunc='day'):
            if date_trunc == 'day':
                trunc_date = functions.TruncDay('record_date')
            elif date_trunc == 'month':
                trunc_date = functions.TruncMonth('record_date')

            return queryset.annotate(
                period=trunc_date
            ).values('period').annotate(
                average_quantity=Avg('quantity')
            ).order_by('period')

        # Queries
        user = User.objects.filter(openid=openid).first()
        if not user:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        
        last_week_data = UricacidRecord.objects.filter(
            user=user,
            record_date__range=[last_week_start, reference_date]
        )
        last_month_data = UricacidRecord.objects.filter(
            user=user,
            record_date__range=[last_month_start, reference_date]
        )
        last_year_data = UricacidRecord.objects.filter(
            user=user,
            record_date__range=[last_year_start, reference_date]
        )

        # Aggregate data and fill missing dates
        weekly_avg = fill_missing_dates(aggregate_uricacid(last_week_data, 'day'), last_week_start, reference_date, 'day')
        monthly_avg = fill_missing_dates(aggregate_uricacid(last_month_data, 'day'), last_month_start, reference_date, 'day')
        yearly_avg = fill_missing_dates(aggregate_uricacid(last_year_data, 'month'), last_year_start, reference_date, 'month')

        summary = {
            'last_week': weekly_avg,
            'last_month': monthly_avg,
            'last_year': yearly_avg
        }

        return JsonResponse({'status': 'success', 'summary': summary})
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

def getFlareupSummary(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reference_date_str = data.get('reference_date')
        openid = data.get('openid')

        reference_date = datetime.datetime.strptime(reference_date_str, '%Y-%m-%d').date()
    
        # Helper function to compute start dates
        def start_date_for_period(days):
            return reference_date - datetime.timedelta(days=days)

        # Helper function to fill in missing dates with 0
        def fill_missing_dates(data, start_date, end_date, date_trunc):
            filled_data = {}
            current_date = start_date
            while current_date <= end_date:
                key = current_date.strftime('%Y-%m-%d') if date_trunc == 'day' else current_date.strftime('%Y-%m')
                filled_data[key] = 0
                current_date += datetime.timedelta(days=1 if date_trunc == 'day' else 30)

            for item in data:
                key = item['period'].strftime('%Y-%m-%d') if date_trunc == 'day' else item['period'].strftime('%Y-%m')
                filled_data[key] = item['average_intensity']

            return [{'period': key, 'average_intensity': value} for key, value in filled_data.items()]

        # Get the starting dates for each period
        last_week_start = start_date_for_period(7)
        last_month_start = start_date_for_period(30)
        last_year_start = start_date_for_period(365)

        # Aggregate average
        def aggregate_flareup(queryset, date_trunc='day'):
            if date_trunc == 'day':
                trunc_date = functions.TruncDay('record_date')
            elif date_trunc == 'month':
                trunc_date = functions.TruncMonth('record_date')

            return queryset.annotate(
                period=trunc_date
            ).values('period').annotate(
                average_intensity=Avg('intense_level')
            ).order_by('period')

        # Queries
        user = User.objects.filter(openid=openid).first()
        if not user:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
        
        last_week_data = FlareupRecord.objects.filter(
            user=user,
            record_date__range=[last_week_start, reference_date]
        )
        last_month_data = FlareupRecord.objects.filter(
            user=user,
            record_date__range=[last_month_start, reference_date]
        )
        last_year_data = FlareupRecord.objects.filter(
            user=user,
            record_date__range=[last_year_start, reference_date]
        )

        # Aggregate data and fill missing dates
        weekly_avg_intensity = fill_missing_dates(aggregate_flareup(last_week_data, 'day'), last_week_start, reference_date, 'day')
        monthly_avg_intensity = fill_missing_dates(aggregate_flareup(last_month_data, 'day'), last_month_start, reference_date, 'day')
        yearly_avg_intensity = fill_missing_dates(aggregate_flareup(last_year_data, 'month'), last_year_start, reference_date, 'month')

        summary = {
            'last_week': weekly_avg_intensity,
            'last_month': monthly_avg_intensity,
            'last_year': yearly_avg_intensity
        }

        return JsonResponse({'status': 'success', 'summary': summary})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})