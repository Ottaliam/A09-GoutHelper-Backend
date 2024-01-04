# myapp/management/commands/add_test_records.py
import random
import datetime
from django.core.management.base import BaseCommand
from user.models import User
from food.models import Food
from records.models import FoodRecord, UricacidRecord, FlareupRecord

class Command(BaseCommand):
    help = 'Adds test records for FoodRecord, UricacidRecord, and FlareupRecord'

    def add_food_records(self, user, food):
        for _ in range(100):
            quantity = random.uniform(0.1, 10.0)  # 随机生成大于0的浮点数
            FoodRecord.objects.create(user=user, food=food, quantity=quantity)

    def add_uricacid_records(self, user):
        for _ in range(100):
            quantity = random.uniform(0.1, 10.0)
            UricacidRecord.objects.create(user=user, quantity=quantity)

    def add_flareup_records(self, user):
        for _ in range(100):
            intense_level = random.randint(1, 5)  # 随机生成1到5的整数
            FlareupRecord.objects.create(user=user, symptom='test', intense_level=intense_level, trigger='test')

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(openid='oX7-M6xsmNloni8r0-xRhNZAx4ic')
        food, _ = Food.objects.get_or_create(name='土豆')

        self.add_food_records(user, food)
        self.add_uricacid_records(user)
        self.add_flareup_records(user)

        self.stdout.write(self.style.SUCCESS('Successfully added test records'))
