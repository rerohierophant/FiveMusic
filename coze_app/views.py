import base64
import os
import random
import re

from django.shortcuts import redirect
from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings

coze_url = "https://api.coze.cn/v1/workflow/run"
coze_headers = {
    "Authorization": "Bearer pat_D7ivM5vVZ0Br8CQAVgnECSoUrGBb7V0OmDU9UR609EWA3zRESONFeEYA3e3GdSBL",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Host": "api.coze.cn",
    "Connection": "keep-alive"
}

session = {}
user_mood = ''
img_explain_result = ''

result_default1 = '''-房子外观描述：房子外观方正，屋顶线条简洁，烟囱细长，整体给人一种简洁而稳定的感觉。
-树外观描述：这棵树是风景画中的树，大树冠，树冠呈云状或球形，树叶浓密，树干粗大，用曲线形线条描画树干表面。
-人外观描述：画中的人外观较为简单，没有过多的细节描绘，可能是一个比较单纯的人。人处于画面的右侧，说明其可能比较关注未来和外部世界。人的身体比例较为协调，没有明显的夸张之处，显示出一种平衡感。人的动作自然，没有特别的紧张或僵硬感，表明其心态较为放松。人的表情不清晰，可能代表其内心世界较为神秘，不太容易被他人了解。人的服装也没有具体描绘，暗示其对自我形象的认知比较模糊。
-心理状态：有干劲但情绪波动大，对外界有警戒心，既想适应社会又在人际交往中有不安。
-相关建议：尝试更加真诚地与他人交流，分享自己的真实想法，同时学会稳定情绪，减少幻想。
-音乐prompt：舒缓的钢琴旋律，夹杂着轻柔的海浪声和鸟鸣声
-用户心情：思'''

result_default2 = '''-房子外观描述：画面中的房子为风景画中的房子，整体比较简化，单线条的屋顶轮廓略显颤抖，不画地面线，房子外观给人一种轻描淡写的感觉。
-树外观描述：很小的树、轻描淡写的树、简化的树、单线条的树、纤细的树干、没有树叶
-人外观描述：单线条的树、轻描淡写的树、小树冠、圆形树冠、没有树叶、简单的单线条树枝。图片中的人看起来比较简单，用单线条勾勒而成，整体给人一种轻描淡写的感觉，如同这棵有着小树冠、圆形树冠、没有树叶且树枝为简单单线条的树一般，简洁而纯粹。
-心理状态：有不切实际的梦想，心情不稳定，易生活在幻想中，天真幼稚且懒惰、行动力差、精力不足，有抑郁倾向，做事追求效率但缺乏坚持性。
-相关建议：尝试将梦想分解为具体可行的小目标逐步实现，提高行动力和坚持性。多参与户外活动，提升精力。关注自己的情绪变化，及时寻求帮助应对抑郁倾向。
-音乐prompt：舒缓的钢琴旋律，夹杂着轻柔的鸟鸣和流水声，营造宁静氛围
-用户心情：忧'''

result_default3 = '''-房子外观描述：房子高大于宽，线条不连续，屋顶房角为锐角，线条为波浪线，重点描绘房子外墙，外墙有污点。
-树外观描述：很小的树，轻描淡写的树，简化的树，单线条的树，树干细而无树冠，没有树叶
-人外观描述：正面像人物，小小的眼睛，没有画眼珠或闭眼，弯弯的眉毛，大大的嘴巴，露出牙齿的嘴巴，圆圆的躯体
-心理状态：用户在生活中有一定干劲和活力，积极主动适应社会且人际关系较好，但同时可能存在一些抑郁、健忘倾向。
-相关建议：保持积极的生活态度，继续发挥适应社会和人际交往的优势。同时，关注自己的情绪变化，当出现抑郁情绪时，及时寻求家人、朋友或专业人士的帮助。
-音乐prompt：舒缓的钢琴旋律，如流水般的音符，营造出宁静平和的氛围，帮助缓解内心的复杂情绪。
-用户心情：思'''

defaults = [result_default1, result_default2, result_default3]


def index(request):
    return render(request, 'index.html')


def paint(request):
    return render(request, 'paint.html')


def loading(request):
    return render(request, 'loading.html')


@csrf_exempt  # 允许 POST 请求不进行 CSRF 验证
def htp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # user_query = data.get('query', '')
        img_base64 = data.get('img_base64', '')

        # 解码 Base64 字符串
        image_data = base64.b64decode(img_base64)

        # 定义保存路径（在 template/static 目录下）
        static_dir = os.path.join(settings.BASE_DIR, 'templates/static/sketch')
        file_path = os.path.join(static_dir, 'uploaded_image.png')

        # 确保目录存在
        os.makedirs(static_dir, exist_ok=True)

        # 保存为 PNG 文件
        with open(file_path, 'wb') as f:
            f.write(image_data)

        smms_headers = {'Authorization': '8cSPTi6b1l4OfqNb61387CYapubYLB2w'}
        files = {'smfile': open(file_path, 'rb')}
        url = 'https://sm.ms/api/v2/upload'
        res = requests.post(url, files=files, headers=smms_headers).json()
        img_url = res['data']['url']
        payload = {
            "bot_id": "7408538615359389746",
            "workflow_id": "7408530827509858313",
            "parameters": {
                "BOT_USER_INPUT": "",
                "img_url": img_url
            }
        }
        response = requests.post(coze_url, headers=coze_headers, json=payload)
        print(response.text)
        data = response.json().get("data")
        result = json.loads(data)["data"]

        print("result]\n")
        print(result)

        session['result'] = result
        session['status'] = 'done'  # 标记处理状态为完成

        return JsonResponse({'status': 'processing'})


def htp_view(request):
    # 从 session 获取结果
    result = session.get('result', '没有结果')  # 如果 result 不存在，返回默认值
    session['status'] = ''
    # 将 result 传递给模板

    # 定义正则表达式来匹配每个部分的描述
    pattern = {
        'house_desc': r"-房子外观描述：(.*?)\n",
        'tree_desc': r"-树外观描述：(.*?)\n",
        'person_desc': r"-人外观描述：(.*?)\n",
        'mental_state': r"-心理状态：(.*?)\n",
        'suggestion': r"-相关建议：(.*?)\n",
        'music_prompt': r"-音乐prompt：(.*?)\n",
        'user_mood': r"-用户心情：(.*)"
    }

    # 使用正则表达式提取信息
    info = {}
    for key, regex in pattern.items():
        match = re.search(regex, result, re.DOTALL)
        if match:
            info[key] = match.group(1).strip()
            print("info-key" + info[key])

    # 提取结果
    house_desc = info.get('house_desc')
    tree_desc = info.get('tree_desc')
    person_desc = info.get('person_desc')
    mental_state = info.get('mental_state')
    suggestion = info.get('suggestion')
    music_prompt = info.get('music_prompt')
    user_mood = info.get('user_mood')

    request.session['user_mood'] = user_mood

    return render(request, 'htp.html', {
        'result': img_explain_result,
        'house_desc': house_desc,
        'tree_desc': tree_desc,
        'person_desc': person_desc,
        'mental_state': mental_state,
        'suggestion': suggestion,
        'music_prompt': music_prompt,
        'user_mood': user_mood
    })


def flower(request):
    return render(request, 'flower.html', {'user_mood': user_mood})


def bigscreen(request):
    return render(request, 'bigscreen.html')


def check_status(request):
    status = session.get('status', 'processing')  # 获取处理状态
    return JsonResponse({'status': status})


def aitalk(request):
    return render(request, "aitalk.html", {'user_mood': user_mood})


@csrf_exempt
def get_coze_suggest(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_query = data.get('user_query', '用户没有输入')

        payload = {
            "bot_id": "7408538615359389746",
            "workflow_id": "7408539358448255026",
            "parameters": {
                "BOT_USER_INPUT": user_query,
            }
        }

        response = requests.post(coze_url, headers=coze_headers, json=payload)
        # print(response.text)
        data = response.json().get("data")
        print(data)
        result = json.loads(data)["data"]
        return JsonResponse({'result': result, 'user_mood': user_mood})
