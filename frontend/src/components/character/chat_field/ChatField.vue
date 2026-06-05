<script setup>
const props=defineProps(['friend'])
const modalRef=useTemplateRef('modal-ref')
function showModal()
{
  modalRef.value.showModal()
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
    <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost bg-transparent absolute right-1 top-1 z-20">✕</button>
    <InputField/>
    <CharacterPhotoField v-if="friend"  :character="friend.character"/>
  </div>
</dialog>
</template>

<style scoped>

</style>
