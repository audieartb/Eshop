<script setup>
import { ref, onMounted } from 'vue'
import { getItems } from '../../services/items'

const data = ref({})

async function setupData() {
  data.value = await getItems()
}

onMounted(() => {
  setupData()
})
</script>
<template>
  <div>
    <v-table fixed-header>
      <thead>
        <tr>
          <th class="text-left">Barcode</th>
          <th class="text-left">Title</th>
          <th class="text-left">Description</th>
          <th class="text-left">Stock</th>
          <th class="text-left">Price</th>
          <th class="text-left">Sold</th>
          <th class="text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.id">
          <td>{{ item.barcode }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.description }}</td>
          <td>{{ item.in_stock }}</td>
          <td>${{ item.sold }}</td>
          <td>{{ item.price }}</td>
          <td>
            <v-btn density="compact" class="mr-1" icon="mdi-file-edit"></v-btn>
            <v-btn density="compact" class="mr-1" icon="mdi-eye"></v-btn>
            <v-btn density="compact" class="mr-1" icon="mdi-delete"></v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>
