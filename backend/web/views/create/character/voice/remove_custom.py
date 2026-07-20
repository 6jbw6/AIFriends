from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.character import Voice, Character
from web.views.create.character.voice.custom.delete_voice import delete_voice


class RemoveCustomVoiceView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            voice_id=request.data['voice_id']
            voice=Voice.objects.get(id=voice_id,owner__user=request.user)
            if Character.objects.filter(voice=voice).exists():
                return Response({
                    'result':'该音色正在被角色使用,请先修改相关角色的音色'
                })
            delete_voice(voice.voice_id)
            if voice.audio:
                voice.audio.delete(save=False)
            voice.delete()
            return Response({
                'result':'success'
            })
        except:
            return Response({
                'result':'系统异常,请稍后重试'
            })
