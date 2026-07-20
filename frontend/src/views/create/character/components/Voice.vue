<script setup>
import api from "@/js/http/api.js";
import {blobToWavFile} from "@/js/utils/blob_to_wav.js";

const props=defineProps(['voices','curVoiceId'])
const emit=defineEmits(['created','deleted'])
const myVoice=ref(props.curVoiceId)

watch( ()=>props.curVoiceId,newVal =>
{
  myVoice.value=newVal
})

const publicVoices=computed(()=>props.voices.filter(v=>!v.is_custom))
const customVoices=computed(()=>props.voices.filter(v=>v.is_custom))
const curVoiceIsCustom=computed(()=>props.voices.some(v=>v.id===myVoice.value&&v.is_custom))

const showCustomPanel=ref(false)
const voiceName=ref('')
const audioFile=ref(null)
const audioUrl=ref('')
const isRecording=ref(false)
const isSubmitting=ref(false)
const message=ref('')

let mediaRecorder=null
let mediaStream=null
let chunks=[]

function setAudio(file)
{
  if(audioUrl.value)
  {
    URL.revokeObjectURL(audioUrl.value)
  }
  audioFile.value=file
  audioUrl.value=file?URL.createObjectURL(file):''
}

function handleFileChange(event)
{
  message.value=''
  const file=event.target.files[0]
  if(!file) return
  if(file.size>10*1024*1024)
  {
    message.value='音频不能超过10MB'
    event.target.value=''
    return
  }
  setAudio(file)
}

async function toggleRecord()
{
  message.value=''
  if(isRecording.value)
  {
    mediaRecorder?.stop()
    return
  }
  try
  {
    mediaStream=await navigator.mediaDevices.getUserMedia({audio:true})
  }
  catch(err)
  {
    message.value='无法访问麦克风,请检查浏览器权限'
    return
  }
  chunks=[]
  mediaRecorder=new MediaRecorder(mediaStream)
  mediaRecorder.ondataavailable=e=>chunks.push(e.data)
  mediaRecorder.onstop=async ()=>
  {
    mediaStream?.getTracks().forEach(t=>t.stop())
    mediaStream=null
    isRecording.value=false
    try
    {
      const blob=new Blob(chunks,{type:mediaRecorder.mimeType})
      const file=await blobToWavFile(blob)
      setAudio(file)
    }
    catch(err)
    {
      message.value='录音处理失败,请重试'
    }
  }
  mediaRecorder.start()
  isRecording.value=true
}

onUnmounted(()=>
{
  mediaStream?.getTracks().forEach(t=>t.stop())
  if(audioUrl.value)
  {
    URL.revokeObjectURL(audioUrl.value)
  }
})

async function handleCreateVoice()
{
  message.value=''
  const name=voiceName.value.trim()
  if(!name)
  {
    message.value='请输入音色名称'
    return
  }
  if(!audioFile.value)
  {
    message.value='请上传或录制一段音频(建议10~20秒清晰人声)'
    return
  }
  isSubmitting.value=true
  try
  {
    const formData=new FormData()
    formData.append('name',name)
    formData.append('audio',audioFile.value)
    const res=await api.post('/api/create/character/voice/create_custom/',formData)
    const data=res.data
    if(data.result==='success')
    {
      emit('created',data.voice)
      voiceName.value=''
      setAudio(null)
      showCustomPanel.value=false
    }
    else
    {
      message.value=data.result
    }
  }
  catch(err)
  {
    message.value='网络异常,请稍后重试'
  }
  finally
  {
    isSubmitting.value=false
  }
}

async function handleDeleteVoice()
{
  if(!curVoiceIsCustom.value) return
  if(!window.confirm('确定删除该自定义音色吗?')) return
  message.value=''
  try
  {
    const res=await api.post('/api/create/character/voice/remove_custom/',{
      voice_id:myVoice.value,
    })
    const data=res.data
    if(data.result==='success')
    {
      emit('deleted',myVoice.value)
    }
    else
    {
      message.value=data.result
    }
  }
  catch(err)
  {
    message.value='网络异常,请稍后重试'
  }
}

defineExpose(
    {
      myVoice
    },
)
</script>

<template>
<fieldset class="fieldset">
  <label class="label text-base">音色</label>
  <div class="flex items-center gap-2">
    <select v-model="myVoice" class="select flex-1">
      <optgroup v-if="publicVoices.length" label="公共音色">
        <option
            v-for="voice in publicVoices"
            :key="voice.id"
            :value="voice.id"
        >{{voice.name}}</option>
      </optgroup>
      <optgroup v-if="customVoices.length" label="我的音色">
        <option
            v-for="voice in customVoices"
            :key="voice.id"
            :value="voice.id"
        >{{voice.name}}</option>
      </optgroup>
    </select>
    <button
        v-if="curVoiceIsCustom"
        type="button"
        class="btn btn-sm btn-outline btn-error"
        @click="handleDeleteVoice()"
    >删除</button>
  </div>
  <button
      type="button"
      class="btn btn-sm btn-outline mt-2 w-fit"
      @click="showCustomPanel=!showCustomPanel"
  >{{showCustomPanel?'收起':'复刻我的音色'}}</button>

  <div v-if="showCustomPanel" class="rounded-box border border-base-300 bg-base-100 p-4 mt-2 flex flex-col gap-3">
    <input
        v-model="voiceName"
        type="text"
        class="input input-sm w-full"
        maxlength="100"
        placeholder="音色名称,如:我的声音"
    />
    <div class="flex items-center gap-2">
      <input
          type="file"
          accept=".wav,.mp3,.m4a,.aac"
          class="file-input file-input-sm flex-1"
          @change="handleFileChange"
      />
      <button
          type="button"
          class="btn btn-sm"
          :class="isRecording?'btn-error':'btn-outline'"
          @click="toggleRecord()"
      >{{isRecording?'停止录音':'在线录音'}}</button>
    </div>
    <p class="text-xs text-base-content/60">上传或录制一段10~20秒的清晰人声,将复刻为你的专属音色</p>
    <audio v-if="audioUrl" :src="audioUrl" controls class="w-full h-8"></audio>
    <p v-if="message" class="text-sm text-red-500">{{message}}</p>
    <button
        type="button"
        class="btn btn-sm btn-neutral w-fit"
        :disabled="isSubmitting"
        @click="handleCreateVoice()"
    >
      <span v-if="isSubmitting" class="loading loading-spinner loading-xs"></span>
      {{isSubmitting?'复刻中...':'开始复刻'}}
    </button>
  </div>
</fieldset>
</template>

<style scoped>

</style>
