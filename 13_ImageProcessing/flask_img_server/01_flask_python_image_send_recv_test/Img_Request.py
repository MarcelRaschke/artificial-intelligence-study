# 참고: https://keraskorea.github.io/posts/2018-10-27-Keras%20%EB%AA%A8%EB%8D%B8%EC%9D%84%20REST%20API%EB%A1%9C%20%EB%B0%B0%ED%8F%AC%ED%95%B4%EB%B3%B4%EA%B8%B0/
# 필수 패키지를 불어옵니다.
import requests

# Keras REST API 엔드포인트의 URL를 입력 이미지 경로와 같이 초기화 합니다.
KERAS_REST_API_URL = "http://localhost:8311/face_predict"
IMAGE_PATH = "강아지.jpg"

# 입력 이미지를 불러오고 요청에 맞게 페이로드(payload)를 구성합니다.
image = open(IMAGE_PATH, "rb").read()
payload = {"image": image}

# 요청을 보냅니다.
r = requests.post(KERAS_REST_API_URL, files=payload).json()

# 요청이 성공했는지 확인합니다.
if r["success"]:
    # 예측을 반복하고 이를 표시합니다.
    # for (i, result) in enumerate(r["predictions"]):
    #     print("{}. {}: {:.4f}".format(i + 1, result["label"],
    #         result["probability"]))
    print('recv success!')

# 그렇지 않다면 요청은 실패합니다.
else:
    print("Request failed")
