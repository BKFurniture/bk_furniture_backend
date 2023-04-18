from rest_framework.views import APIView
from rest_framework.response import Response


from .BKF_chatbot import WebappConfig


class ChatbotView(APIView):

    def post(self, request):
        message = request.data.get('message')
        response = WebappConfig.chatbot.answer_question(message)
        return Response({'response': response})
