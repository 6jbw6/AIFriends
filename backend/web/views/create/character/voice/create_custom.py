import uuid

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Voice
from web.models.user import UserProfile
from web.views.create.character.voice.custom.create_voice import create_voice

MAX_AUDIO_SIZE=10*1024*1024
MAX_CUSTOM_VOICE_COUNT=10
ALLOWED_EXTS=['wav','mp3','m4a','aac']


class CreateCustomVoiceView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            user_profile=UserProfile.objects.get(user=request.user)
            name=request.data['name'].strip()[:100]
            audio=request.FILES.get('audio',None)
            if not name:
                return Response({
                    'result':'音色名称不能为空'
                })
            if not audio:
                return Response({
                    'result':'音频不能为空'
                })
            if audio.size>MAX_AUDIO_SIZE:
                return Response({
                    'result':'音频不能超过10MB'
                })
            ext=audio.name.split('.')[-1].lower()
            if ext not in ALLOWED_EXTS:
                return Response({
                    'result':'仅支持 wav / mp3 / m4a / aac 格式'
                })
            if Voice.objects.filter(owner=user_profile).count()>=MAX_CUSTOM_VOICE_COUNT:
                return Response({
                    'result':f'最多创建{MAX_CUSTOM_VOICE_COUNT}个自定义音色'
                })
            voice=Voice(name=name,voice_id='',owner=user_profile)
            voice.audio.save(f'{uuid.uuid4().hex[:10]}.{ext}',audio,save=False)
            audio_url=settings.MEDIA_URL+voice.audio.name
            res=create_voice(audio_url,f'u{request.user.id}')
            voice_id=res.get('output',{}).get('voice_id')
            if not voice_id:
                voice.audio.delete(save=False)
                return Response({
                    'result':'音色复刻失败,请更换音频后重试'
                })
            voice.voice_id=voice_id
            voice.save()
            return Response({
                'result':'success',
                'voice':{
                    'id':voice.id,
                    'name':voice.name,
                    'is_custom':True,
                },
            })
        except:
            return Response({
                'result':'系统异常,请稍后重试'
            })
