from decouple import config
from http import HTTPStatus

from common.helpers.http_client import http_get


class ChatbotService:
    def __init__(self):
        pass


    def get_chatbot_output(self, user_input: str) -> str:
        try:
            response = http_get(
                url=f"{config('CHATBOT_API_URL')}/api/v1/agent/chatbot/",
                params={"query": user_input}
            )

            decoded = response.json()

            if decoded['code'] == HTTPStatus.OK.value:
                output = decoded['data']

            else:
                print("ERROR: ", response, decoded)
                output = "답변을 생성하지 못했습니다 😅"

            return output

        except Exception as e:
            return f"관리자에게 문의해 주세요 {str(e)}"