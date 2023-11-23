import requests
import logging
import json

from django.http import JsonResponse
from .models import User

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code', None)
        
        if code:
            appid = 'wxf748ebc5e8814741'
            secret = '6332b3b4d1f1151b8c9a094b5484d251'
            url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                openid = data.get('openid', None)
                session_key = data.get('session_key', None)

                if openid and session_key:
                    # 检查用户是否存在，不存在则创建
                    user, created = User.objects.get_or_create(openid=openid)
                    user.session_key = session_key

                    return JsonResponse({'status': 'success', 'openid': openid})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Fail to obtain openid and session_key'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Fail at WeChat API'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid Code'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
