<script setup>
import { ref, onMounted, computed, watch, onBeforeMount } from 'vue'
import { getItems, getCount, itemsPagination } from '../../services/items'

const data = ref({})
const limit = ref(5)
const skip = ref(0)
const pageStart = ref(0)
const pageEnd = ref(limit - 1)
const tableData = ref([])
const products = ref([])
const productCount = ref(null)
const currentPage = ref()

const pages = computed(() => {
  console.log('computed', productCount.value)
  return Math.ceil(productCount.value / limit.value)
})

watch(currentPage, async (newCurrentPage, oldCurrentPage) => {
  let start = (newCurrentPage - 1) * limit.value
  let end = newCurrentPage * limit.value
  let len = products.value.length
  if (start >= len) {
    await loadData(len, (end - len))
  }
  tableData.value = products.value.slice(start, end)
})

async function loadData(start, end) {
  data.value = await itemsPagination(start, end)
  products.value = products.value.concat(data.value)
  tableData.value = products.value.slice(start, end)
}

async function getProductCount() {
  if (!productCount.value) {
    const res = await getCount()
    productCount.value = res.data.count
  }
}

async function setupData() {
  data.value = await itemsPagination(skip.value, limit.value)
  tableData.value = data.value
  products.value = data.value
  skip.value = tableData.value.length
}

onMounted(() => {
  getProductCount()
  setupData()
})
</script>
<template>
  <div class="ml-4">
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
        <tr v-for="item in tableData" :key="item.id">
          <td>{{ item.barcode }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.description }}</td>
          <td>{{ item.in_stock }}</td>
          <td>${{ item.price }}</td>
          <td>{{ item.sold }}</td>
          <td>
            <v-btn density="compact" class="mr-1" icon="mdi-file-edit"></v-btn>
            <v-btn density="compact" class="mr-1" icon="mdi-eye"></v-btn>
            <v-btn density="compact" class="mr-1" icon="mdi-delete"></v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    <div class="d-flex justify-center">
      <v-pagination
        :length="pages"
        v-model="currentPage"
        total-visible="5"
        :start="1"
      ></v-pagination>
    </div>
    <div class="d-flex justify-center">
    </div>
  </div>
</template>
