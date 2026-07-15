<script setup>
const props=defineProps(['friend'])
const modalRef=useTemplateRef('modal-ref')
const inputRef=useTemplateRef('input-ref')
const chatHistoryRef=useTemplateRef('chat-history-ref')
const history=ref([])

async function showModal()
{
  modalRef.value.showModal()
  await nextTick()
  inputRef.value.focus()
}
defineExpose({
  showModal,
})
const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})

function handlePushBackMessage(msg)
{
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom()
}

function handleAddToLastMessage(delta)
{
  history.value.at(-1).content+=delta
  chatHistoryRef.value.scrollToBottom()
}
function handlePushFrontMessage(msg)
{
  history.value.unshift(msg)
}
</script>

<template>
<dialog ref="modal-ref" class="modal">
  <div class="modal-box w-90 h-150 relative overflow-hidden p-0" :style="modalStyle">
    <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost bg-transparent absolute right-1 top-1">✕</button>
    <ChatHistory
        ref="chat-history-ref"
        v-if="friend"
        :history="history"
        :friendId="friend.id"
        :character="friend.character"
    />
    <InputField
        v-if="friend"
        ref="input-ref"
        :friendId="friend.id"
        @pushBackMessage="handlePushBackMessage"
        @addToLastMessage="handleAddToLastMessage"
        @PushFrontMessage="handlePushFrontMessage"
    />
    <CharacterPhotoField v-if="friend"  :character="friend.character"/>
  </div>
</dialog>
</template>

<style scoped>

</style>
