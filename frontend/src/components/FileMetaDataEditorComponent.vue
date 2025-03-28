<template>
  <div class="d-flex flex-column" style="width: 20em">
    <input
      type="text"
      class="form-control mb-2"
      placeholder="Title"
      v-model="formModal.title"
    />
    <textarea
      type="text"
      class="form-control mb-2"
      placeholder="Description (optional)"
      v-model="formModal.description"
    />
    <ul class="form-control d-flex flex-wrap">
      <li v-for="(author, index) in formModal.authors" class="px-1 m-1" :key="author">
        {{ author }}
        <button type="button" class="p-0 btn text-secondary" @click.prevent="deleteAuthor(index)">
          <font-awesome-icon icon="fa-regular fa-circle-xmark" />
        </button>
      </li>
      <input
        type="text"
        class="flex-grow-1 border-0"
        :placeholder="formModal.authors.length == 0 ? 'One author per line, validate with ⏎' : ''"
        @keyup.enter="addAuthor"
      />
    </ul>
    <input type="text" class="form-control" placeholder="filename" v-model="formModal.filename" />
  </div>
</template>
<script setup lang="ts">
import type { FileMetadataForm, MetadataEditorFormType } from '@/constants'
import { ref, watch, type Ref } from 'vue'
const props = defineProps<{
  metadata: FileMetadataForm
}>()

const formModal: Ref<MetadataEditorFormType> = ref({
  title: props.metadata.title,
  description: props.metadata.description,
  authors: props.metadata.authors,
  filename: props.metadata.filename
})

const emit = defineEmits<{
  updateForm: [MetadataEditorFormType]
}>()

watch(
  formModal,
  async (newValue) => {
    emit('updateForm', newValue)
  },
  { deep: true }
)

async function addAuthor(event: Event) {
  event.preventDefault()
  const target = event.target as HTMLInputElement
  const value = target.value.trim()
  if (value.length != 0) {
    formModal.value.authors.push(target.value)
    target.value = ''
  }
}

async function deleteAuthor(index: number) {
  formModal.value.authors = formModal.value.authors.filter((_, i) => i !== index)
}
</script>
<style scoped>
ul li {
  color: #333;
  list-style: none;
  border-radius: 5px;
  background: #f2f2f2;
}

ul input {
  outline: none;
  font-size: 16px;
}
</style>
