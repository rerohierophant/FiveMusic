import requests
import json
import re

url = "https://api.coze.cn/v1/workflow/run"
headers = {
    "Authorization": "Bearer pat_5qT5weHV5EmXifvWEyAwYCRJhT0MzAihFgNVw1meH0qL0IsTlhFtAURFhSzGJwKM",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Host": "api.coze.cn",
    "Connection": "keep-alive"
}

payload = {
    "bot_id": "7408538615359389746",
    "workflow_id": "7408530827509858313",
    "parameters": {
        "BOT_USER_INPUT": "",
        "img_url": 'https://s2.loli.net/2024/08/30/dBO9cXo5PLHKSF1.png'
    }
}

# response = requests.post(url, headers=headers, json=payload)
# data = response.json().get("data")
# print(json.loads(data)["data"])
#
# result = json.loads(data)["data"]
result = '''-房子外观描述：图中的房子是一座有三角形屋顶、两个窗户、一扇门且整体线条较为清晰的房子，看起来较为稳固。
-树外观描述：这棵树位于画面右侧，树干较为粗壮，树枝向左伸展，树叶比较茂密，整体呈现出蓬勃向上的生长态势。
-人外观描述：画面中的人留着短发，穿着短袖和短裤，没有明显的面部表情，身形较为矮小，双手自然下垂，双脚并拢站立。
-心理状态：行动能力较强但缺乏幻想力且智力被认为低下，同时有退缩倾向、情绪低落、对生活失望。
-相关建议：尝试进行一些富有创意的活动，如绘画、写作等，以激发幻想力。多与积极乐观的人交流，调整心态，重新找回对生活的热情。
-音乐prompt：舒缓的钢琴旋律，伴随着轻柔的海浪声和鸟鸣声
-用户心情：忧
'''

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

# 提取结果
house_desc = info.get('house_desc')
tree_desc = info.get('tree_desc')
person_desc = info.get('person_desc')
mental_state = info.get('mental_state')
suggestion = info.get('suggestion')
music_prompt = info.get('music_prompt')
user_mood = info.get('user_mood')

# 输出结果
print("房子外观描述:", house_desc)
print("树外观描述:", tree_desc)
print("人外观描述:", person_desc)
print("心理状态:", mental_state)
print("相关建议:", suggestion)
print("音乐prompt:", music_prompt)
print("用户心情:", user_mood)
