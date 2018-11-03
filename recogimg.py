import base64
import json
import sys
from requests import Request, Session

def recognize_captcha(str_image_path):
        bin_captcha = open(str_image_path, 'rb').read()
        str_encode_file = base64.b64encode(bin_captcha).decode("utf-8")
        str_url = "https://vision.googleapis.com/v1/images:annotate?key="
        str_api_key = "自分のAPIKEYを入力する"
        str_headers = {'Content-Type': 'application/json'}
        str_json_data = {
            'requests': [
                {
                    'image': {
                        'content': str_encode_file
                    },
                    'features': [
                        {
                            'type': "TEXT_DETECTION",
                            'maxResults': 10
                        }
                    ]
                }
            ]
        }
        print("リクエスト開始")
        obj_session = Session()
        obj_request = Request("POST",
                              str_url + str_api_key,
                              data=json.dumps(str_json_data),
                              headers=str_headers
                              )
        obj_prepped = obj_session.prepare_request(obj_request)
        obj_response = obj_session.send(obj_prepped,
                                        verify=True,
                                        timeout=60
                                        )
        print("リクエスト終了")

        if obj_response.status_code == 200:
            print("画像の認識に成功しました")
            return obj_response.text
        else:
            print("画像の認識に失敗しました")
            return obj_response.text

if __name__ == '__main__':
    recog_img_filename = sys.argv[1]
    save_json_filename = "recog.json"
    save_maintext_filename = "recog.txt"

    #save got json file
    result = recognize_captcha(recog_img_filename)
    json_dict = json.loads(result)
    fp = open(save_json_filename, 'w')
    json.dump(json_dict, fp, ensure_ascii=False, indent=2, sort_keys=True)
    print("解析結果をjsonファイルとして保存しました")

    #save recognize result as textfile
    data = json_dict['responses'][0]['fullTextAnnotation']['text']
    with open(save_maintext_filename, "w") as f:
        f.write(data)
    print("認識した文字列をテキストファイルとして保存しました")
