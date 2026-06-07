<script setup>
const props=defineProps(['friend'])
const modalRef=useTemplateRef('modal-ref')
const inputRef=useTemplateRef('input-ref')
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
</script>

<template>
<dialog ref="modal-ref" class="modal">
  <div class="modal-box w-90 h-150 relative overflow-hidden p-0" :style="modalStyle">
    <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost bg-transparent absolute right-1 top-1">✕</button>
    <InputField v-if="friend"
        ref="input-ref"
        :friendId="friend.id"
    />
    <CharacterPhotoField v-if="friend"  :character="friend.character"/>
  </div>
</dialog>
</template>

<style scoped>

</style>
