from flask import Flask, jsonify
import requests

app = Flask(__name__)

# 정보 가져오기
def fetch_meal_info():
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
        'MLSV_YMD': '20230821', 
        'MMEAL_SC_CODE': 2
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

    # 가져온 정보를 JSON 형식으로 리턴
    return jsonify(meal_info)

# 패키징을 따로 진행하니 삭제하고 Procfile로 대체
#if __name__ == '__main__':
    #app.run(port=8000)