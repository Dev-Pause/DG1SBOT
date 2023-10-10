
# 세로출력이 가능한 급식봇 최종 완성

from flask import Flask, jsonify, request
import requests
from datetime import date, datetime
import time
import pytz

app = Flask(__name__)

# IP 주소와 마지막 요청 시간을 저장할 데이터 구조 (딕셔너리)
request_history = {}

# 임계값 설정 (예: 2초)
threshold = 2



# 정보 가져오기
def fetch_meal_info(meal_code):
    
    # 현재 날짜와 시간 가져오기
    now = datetime.now()
    # 한국 표준시 타임존 설정
    korea_timezone = pytz.timezone('Asia/Seoul')
    # 한국 표준시로 변환
    korea_time = now.astimezone(korea_timezone)
    # 오늘 날짜 계산 (YYYYMMDD 형식)
    today = korea_time.strftime("%Y%m%d")

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
            menu_list = []

            for meal in meals:
                menu_name = meal.get('DDISH_NM', '')
                # 알레르기 정보가 포함된 숫자들을 제거하여 메뉴만 추출
                menu_name_without_allergy = menu_name.split("(")[0].strip()
                menu_list.append(menu_name_without_allergy)

            return {"menu": menu_list}

        return {"error": "Failed to fetch meal information."}

    except Exception as e:
        return {"error": str(e)}




@app.route('/get_meal', methods=['POST'])

def get_meal():
    # 클라이언트의 IP 주소 가져오기
    ip_address = request.remote_addr
    
    # 이전에 저장된 데이터에서 동일한 IP 주소가 있는지 확인
    if ip_address in request_history:
        last_request_time = request_history[ip_address]
        current_time = time.time()
        
        # 현재 시간과 이전 요청 시간 사이의 차이 계산
        time_diff = current_time - last_request_time
        
        # 임계값보다 작은 경우 추가 처리를 무시하고 응답 반환
        if time_diff < threshold:
            response_json ={
                "version": "2.0",
                "template":{
                    "outputs":[ 
                        {
                            "simpleText" : {
                                "text" : "한번에 많은 요청을 보내지 마세요"
                            }
                        }
                    ]
                }
            }
            return jsonify(response_json)
     
     # 새로운 요청에 대해 현재 시간으로 업데이트
    request_history[ip_address] = time.time()   
        
        
        
    #meal_code = request.json.get('meal_code')  # 'meal_code'에 해당하는 값 가져오기
    #meal_code = request.json['params']['meal_code']
    meal_code = request.json['action']['params']['meal_code']

    
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
        # menu_str = "\n".join(meal_info['''menu'''])
        menu_str = "<br/>".join(meal_info['menu']).replace("<br/>", "\n")
        
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





























'''# 세로출력이 가능한 급식봇 최종 완성

from flask import Flask, jsonify, request
import requests
from datetime import date

app = Flask(__name__)


# 정보 가져오기
def fetch_meal_info(meal_code):
    # 오늘 날짜 구하기
    today = date.today().strftime("%Y%m%d")

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
    
    #meal_code = request.json.get('meal_code')  # 'meal_code'에 해당하는 값 가져오기
    #meal_code = request.json['params']['meal_code']
    meal_code = request.json['action']['params']['meal_code']

    
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
        # menu_str = "\n".join(meal_info['menu'])
        menu_str = "<br/>".join(meal_info['menu']).replace("<br/>", "\n")
        
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


#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################






















# 아침 점심 저녁 모두 출력가능한 완성본
'''from flask import Flask, jsonify, request
import requests
from datetime import date

app = Flask(__name__)



# 정보 가져오기
def fetch_meal_info(meal_code):
    # 오늘 날짜 구하기
    today = date.today().strftime("%Y%m%d")

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
        'MLSV_YMD': '20230822',
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
    
    #meal_code = request.json.get('meal_code')  # 'meal_code'에 해당하는 값 가져오기
    #meal_code = request.json['params']['meal_code']
    meal_code = request.json['action']['params']['meal_code']

    
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
        # 메뉴 이름이 담긴 리스트를 개행 문자로 연결하여 하나의 문자열로 재구성.
        menu_str = "\n".join(meal_info["menu"])

        # 카카오 i 오픈빌더 응답 형식에 맞춰 JSON 응답 생성.
        response_json ={
            "version": "2.0",
            "template":{
                "outputs":[
                    {
                        "simpleText":{
                            "text": menu_str   # 메뉴 이름이 담긴 문자열
                        }
                    }
                ]
            }
        }

    return jsonify(response_json)   # 생성한 JSON 응답 반환.'''
































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