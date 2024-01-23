<script setup>
import { ref } from 'vue'
import { importFile } from '../../services/adminLogin'

const files = ref()
const acceptedFileType = ['text/csv', 'application/json']

async function submitFile() {
  const file = files.value.files[0]

  if (acceptedFileType.includes[file.type]) {
    return
  }

  const form_data = new FormData()
  form_data.append('file', file)
  await importFile(form_data)
}
</script>

<template>
  <div class="d-flex">
    <div class="w-50">
      <div class="mb-5">
        <h2>Select a .CSV/.JSON file to upload</h2>
      </div>
      <div>
        <v-file-input label="File input" ref="files" variant="outlined"></v-file-input>
        <div class="d-flex justify-end">
          <v-btn color="orange" @click="submitFile"> Submit </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
