from django.test import TestCase, Client
from django.urls import reverse
from .models import Food
import json
import base64

class FoodTests(TestCase):
    def setUp(self):
        # 创建测试客户端
        self.client = Client()

        # 添加一些测试食品数据
        Food.objects.create(name="Apple", ms_unit="g", purine_per_unit=10, health_tip="Good for health")
        Food.objects.create(name="Banana", ms_unit="g", purine_per_unit=5, health_tip="Rich in potassium")

        # 设置URLs
        self.search_url = reverse('search')
        self.get_food_url = reverse('get')

    def test_search_food_post(self):
        # 测试 POST 请求
        response = self.client.post(self.search_url, json.dumps({'name': 'Apple'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue('Apple' in str(response.content))

    def test_search_food_invalid_method(self):
        # 测试非 POST 请求
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

    def test_get_food_by_name_post(self):
        # 测试 POST 请求
        response = self.client.post(self.get_food_url, json.dumps({'name': 'Banana'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue('Banana' in str(response.content))

    def test_get_food_by_name_not_found(self):
        # 测试查找不存在的食品
        response = self.client.post(self.get_food_url, json.dumps({'name': 'Orange'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

    def test_get_food_by_name_invalid_method(self):
        # 测试非 POST 请求
        response = self.client.get(self.get_food_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

    def tearDown(self):
        # 清理代码
        pass
