import PIL.Image
import re
import os
from decouple import config
from io import BytesIO
from gtts import gTTS

import google.generativeai as genai
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import JsonResponse, FileResponse

class ImageConvertAPIView(APIView):
    def post(self, request):
        img = request.data.get('image')
        image = PIL.Image.open(img)
        
        GOOGLE_API_KEY = config('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel('gemini-pro-vision')

        # 요약본
        response = model.generate_content(["위 그림에 대해 항목별로 요약해서 설명해줘. ", image], stream=True)
        response.resolve()
        summary = response.text.replace('•', '  *')
        summary = re.sub(r'\*\*', '', summary)
        summary = re.sub(r'- ', '', summary)
        summary = summary.strip()
        summary = summary.split('\n')
        summary = [item for item in summary if item != '']

        # 전문
        response = model.generate_content(["위 그림의 모든 글씨를 알려줘. ", image], stream=True)
        response.resolve()
        all = response.text.replace('•', '  *')
        all = re.sub(r'\*\*', '', all)
        all = re.sub(r'- ', '', all)
        all = all.strip()
        all_text = all

        # tts
        tts = gTTS(text=all, lang= "ko")
        tts.save("voice.mp3")
        voice_file_path = os.path.abspath('voice.mp3')

        all = all.split('\n')
        all = [item for item in all if item != '']

        return Response({"summary": summary, "all" : all, "file_path" : voice_file_path, "all_text" : all_text})
    
