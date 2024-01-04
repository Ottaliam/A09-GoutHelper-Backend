import datetime
import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Food, FoodRecord, UricacidRecord, FlareupRecord

class RecordTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create test data
        self.user = User.objects.create(openid="testuser")
        self.food = Food.objects.create(name="Test Food", ms_unit="g", purine_per_unit=10, health_tip="Test Tip")
        self.add_food_record_url = reverse('add_food_record')
        self.get_food_record_summary_url = reverse('food_record_summary')
        self.get_food_records_for_date_url = reverse('get_records_for_date')
        self.add_uricacid_record_url = reverse('add_uricacid_record')
        self.get_uricacid_summary_url = reverse('uricacid_record_summary')
        self.add_flareup_record_url = reverse('add_flareup_record')
        self.get_flareup_summary_url = reverse('flareup_record_summary')

    def test_add_food_record_success(self):
        # Test successful food record addition
        data = {
            'openid': self.user.openid,
            'food_name': self.food.name,
            'quantity': 100,
            'record_date': '2023-01-01'
        }
        response = self.client.post(self.add_food_record_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_get_food_record_summary(self):
        # Test fetching food record summary
        data = {'openid': self.user.openid, 'reference_date': '2023-01-01'}
        response = self.client.post(self.get_food_record_summary_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_get_food_records_for_date(self):
        # Test fetching food records for a specific date
        data = {'openid': self.user.openid, 'date': '2023-01-01'}
        response = self.client.post(self.get_food_records_for_date_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_add_uricacid_record_success(self):
        data = {
            'openid': self.user.openid,
            'quantity': 5.0,
            'record_date': '2023-01-01'
        }
        response = self.client.post(self.add_uricacid_record_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue('record_id' in response_data)
        record_id = response_data['record_id']
        self.assertTrue(UricacidRecord.objects.filter(id=record_id).exists())

    def test_get_uricacid_summary(self):
        data = {'openid': self.user.openid, 'reference_date': '2023-01-01'}
        response = self.client.post(self.get_uricacid_summary_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('last_week', response_data['summary'])
        self.assertIn('last_month', response_data['summary'])
        self.assertIn('last_year', response_data['summary'])

    def test_add_flareup_record_success(self):
        data = {
            'openid': self.user.openid,
            'symptom': 'Test Symptom',
            'intense_level': 3,
            'trigger': 'Test Trigger',
            'record_date': '2023-01-01'
        }
        response = self.client.post(self.add_flareup_record_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue('record_id' in response_data)
        record_id = response_data['record_id']
        self.assertTrue(FlareupRecord.objects.filter(id=record_id).exists())

    def test_get_flareup_summary(self):
        data = {'openid': self.user.openid, 'reference_date': '2023-01-01'}
        response = self.client.post(self.get_flareup_summary_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('last_week', response_data['summary'])
        self.assertIn('last_month', response_data['summary'])
        self.assertIn('last_year', response_data['summary'])


    def tearDown(self):
        # Clean up after tests
        pass
