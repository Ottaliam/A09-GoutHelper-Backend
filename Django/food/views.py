import base64
import uuid

from django.http import JsonResponse
from django.core.files.base import ContentFile

from .models import Food

def add_food(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ms_unit = request.POST.get('ms_unit')
        purine_per_unit = request.POST.get('purine_per_unit', 0.0)
        health_tip = request.POST.get('health_tip')
        image_data = request.POST.get('image')

        # Handle the image data
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")
        else:
            image = None

        try:
            food = Food.objects.create(
                name=name,
                ms_unit=ms_unit,
                purine_per_unit=purine_per_unit,
                health_tip=health_tip,
                image=image
            )
            return JsonResponse({'status': 'success', 'food_id': food.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
