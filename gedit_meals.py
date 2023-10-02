from flask import Flask, jsonify, request
import requests
from datetime import date

app = Flask(__name__)



# 정보 가져오기
def fetch_meal_info(meal_code):
    # 오늘 날짜 구하기
    today = int(date.today().strftime("%Y%m%d"))

    # API 엔드포인트 및 파라미터 설정
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    service_key = "c9d9e1cde8b54de786c94fcc0e5eae36"
    
    meal_code_mapping = {
        "아침": "1",
        "점심": "2",
        "저녁": "3"
    }
    
    params = {
        'KEY': service_key,
        'Type': 'json',
        'pIndex': '1',
        'pSize': '100',
        'ATPT_OFCDC_SC_CODE': 'D10',
        'SD_SCHUL_CODE': '7240331',
        'MLSV_YMD': str(today),
        'MMEAL_SC_CODE': meal_code_mapping.get(meal_code)
    }

    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            meals = data['mealServiceDietInfo'][1]['row']
            meal_names = [meal.get('DDISH_NM', '') for meal in meals]
            return {"menu": meal_names}
        
        return {"error": "Failed to fetch meal information."}
        
    except Exception as e:
        return {"error": str(e)}




@app.route('/get_meal', methods=['POST'])

def get_meal():
    meal_code = request.form.get('meal_code')  # 'meal_code'에 해당하는 값 가져오기
    
    if meal_code is None:
        response_json ={
            "version": "2.0",
            "template":{
                "outputs":[ 
                    {
                        "simpleText" : {
                            "text" : "'meal_code' parameter is missing."
                        }
                    }
                ]
            }
        }
        return jsonify(response_json)
    
    meal_info = fetch_meal_info(meal_code)
    
    if "error" in meal_info:
        # 에러 메시지가 있는 경우
        response_json ={
            "version": "2.0",
            "template":{
                "outputs":[ 
                    {
                        "simpleText" : {
                            "text" : "급식 정보가 없습니다"
                        }
                    }
                ]
            }
        }

    else:
        # 메뉴 이름이 담긴 리스트를 개행 문자로 연결하여 하나의 문자열로 만듦.
        menu_str = "\n".join(meal_info["menu"])

        # 카카오 i 오픈빌더 응답 형식에 맞춰 JSON 응답 생성.
        response_json ={
            "version": "2.0",
            "template":{
                "outputs":[
                    {
                        "simpleText":{
                            "text": menu_str   # 메뉴 이름이 담긴 문자열을 여기에 넣음.
                        }
                    }
                ]
            }
        }

    return jsonify(response_json)   # 생성한 JSON 응답 반환.
































'''# 오늘 날짜 적용까지 가능한 완전본
from flask import Flask, jsonify
import requests
from datetime import date

app = Flask(__name__)




# 정보 가져오기
def fetch_meal_info():
    
    #오늘 날짜 구하기
    today = int(date.today().strftime("%Y%m%d"))
    
    # API 엔드포인트 및 파라미터 설정
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    service_key = "c9d9e1cde8b54de786c94fcc0e5eae36"
    params = {
        'KEY': service_key,
        'Type': 'json',
        'pIndex': '1',
        'pSize': '100',
        'ATPT_OFCDC_SC_CODE': 'D10',
        'SD_SCHUL_CODE': '7240331',
        'MLSV_YMD': '20230822',
        'MMEAL_SC_CODE': '2'
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            meals = data['mealServiceDietInfo'][1]['row']
            meal_names = [meal.get('DDISH_NM', '') for meal in meals]
            return {"menu": meal_names}
        else:
            return {"error": "Failed to fetch meal information."}
        
    except Exception as e:
         return {"error": str(e)}





@app.route('/get_meal', methods=['POST'])
def get_meal():
    
    # 정보를 가져오는 함수 호출
    meal_info = fetch_meal_info()
    
    
    if "error" in meal_info :
        # 에러 메시지가 있는 경우
        response_json ={
            "version": "2.0",
            "template":{
                "outputs":[ 
                    {
                        "simpleText" : {
                            "text" : " 급식 정보가 없습니다"
                        }
                    }
                ]
            }
        }

    else:

        # 메뉴 이름이 담긴 리스트를 개행 문자로 연결하여 하나의 문자열로 만듦.
        menu_str = "\n".join(meal_info["menu"])

        # 카카오 i 오픈빌더 응답 형식에 맞춰 JSON 응답 생성.
        response_json ={
            "version": "2.0",
            "template":{
                "outputs":[
                    {
                            "simpleText":{
                                "text": menu_str   # 메뉴 이름이 담긴 문자열을 여기에 넣음.
                            }
                    }
                ]
            }
        }

    return jsonify(response_json)   # 생성한 JSON 응답 반환.'''