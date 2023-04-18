# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions

# from .BKF_chatbot import ChatBot
# # Create your views here.


# class ChatbotView(APIView):
#     chatbot = ChatBot()

#     def post(self, request):
#         message = request.data.get('message')
#         response = self.chatbot.answer_question(message)
#         return Response({'response': response})
