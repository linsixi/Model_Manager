import requests
import json
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import base64

def personalized_api():
    print( '请给出你的请求文件' )
    with open( '../params.json', 'r', encoding='utf-8' ) as f:
        info = json.load( f )
        api = info["api"]
        print( api )
        params = info["params"][0]
        print( params )
        headers = info["headers"][0]
        print( headers )
    response = requests.post( api, json=params, headers=headers, stream=False )
    if response.status_code == 200:
        response_json = response.json()
        with open( '../response.json', 'w', encoding='utf-8' ) as f:
            json.dump( response_json, f, indent=4, ensure_ascii=False )
    else:
        body = response.content.decode('utf-8')
        print(f'request failed,status_code:{response.status_code},body:{body}')



def get_access_token_qianfan():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=DTNX9fIESYPHsOLYRSgGEPBJ&client_secret=PUfU7ew9kXJOBpZRzlmkY3OBRZ7ksB1m"
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def get_zidongtaichu( question, per ):
    # 紫东太初文本生成
    api = 'https://ai-maas.wair.ac.cn/maas/v1/chat/completions'
    headers = { 'Authorization': 'Bearer tlf3tc8sltk89etyx0p16u5p' }
    params = {
        'model': 'taichu_llm',
        'messages': [{"role": "user", "content": f"'{question}':{per}"}],
        'stream': False
    }

    response = requests.post(api, json=params, headers=headers, stream=True)
    if response.status_code == 200:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        return content
    else:
        body = response.content.decode('utf-8')
        print(f'request failed,status_code:{response.status_code},body:{body}')


def get_qianfan_text( question, per ):
    # 千帆文本生成
    access_token = get_access_token_qianfan()
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + str(access_token)
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"'{question}':{per}"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload )
    if response.status_code == 200:
        response_json = response.json()
        content = response_json[ 'result' ]
        return content
    else:
        body = response.content.decode('utf-8')
        print(f'request failed,status_code:{response.status_code},body:{body}')


def get_qianfan_graph( question, per ):
    access_token = get_access_token_qianfan()
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image/sd_xl?access_token=" + str( access_token )
    payload = json.dumps({
        "prompt": f"'{question}':{per}",
        "size": "1024x1024",
        "n": 1,
        "steps": 20,
        "sampler_index": "Euler a"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        body = response.content.decode('utf-8')
        print(f'request failed,status_code:{response.status_code},body:{body}')
    response_dict = response.json()
    b64_image = response_dict['data'][0]['b64_image']

    # # plt显示图片
    # image_data = base64.b64decode( b64_image )
    # image = Image.open(BytesIO(image_data))
    # plt.imshow( image )
    # plt.axis('off')
    # plt.show()

def get_qianfan_read( question, per ):
    access_token = get_access_token_qianfan()
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/image2text/fuyu_8b?access_token=" + access_token
    question = image_to_base64( question )

    payload = json.dumps( {
        "prompt": f"{per}",
        "image": f"{question}"
    } )
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request( "POST", url, headers = headers, data = payload )
    response_dict = response.json()
    return response_dict[ 'result' ]

def image_to_base64( image_path ):
    with open( image_path, "rb" ) as image_file:
        image_data = image_file.read()
        base64_encoded = base64.b64encode( image_data ).decode( 'utf-8' )
        return base64_encoded





def choice( n ):
    switcher = {
        '1':'千帆大模型文本功能',
        '2':'紫东太初大模型文本功能',
        '3':'千帆大模型图片生成功能',
        '4':'千帆大模型图片解析功能',
        '5':'用户自定义api'
    }

    return switcher.get( n, '没有该功能' )


def main():
    '''
    n = input( '需要的功能:' )                        # 需要模型的编号
    per = input( '输入想问的问题：')                   # 用户对于结果自定义的提问

    question = input( 'question: ' )                # 模型输出的文本结果

    '''
    n = 5
    per = '这是什么'
    question = '苹果'
    n = str( n )
    need = choice( n )
    print(f'我是{need}，正在对模型的输出结果进行最后一步处理...')
    if n != '5':
        if n == '1':
            result = get_qianfan_text( question, per )
        elif n == '2':
            result = get_zidongtaichu( question, per )
        elif n == '3':
            result = get_qianfan_graph( question, per )
        elif n == '4':
            result = get_qianfan_read( question, per )
        print('处理完成！')
        print(result)
    else:
        personalized_api()
        print( '处理完成！' )


if __name__ == '__main__':
    main()
