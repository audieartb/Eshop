<script setup>
import { ref, onMounted, computed, watch, onBeforeMount } from 'vue'
import { getItems, getCount, itemsPagination } from '../../services/items'
import {useAdminStore} from '../../stores/admin'
import router from '../../router';

const adminStore = useAdminStore()

const limit = ref(5)
const skip = ref(0)
const tableData = ref([])
const products = ref([])
const productCount = ref(null)
const currentPage = ref()


const pages = computed(() => {
  //Calculates how many pages based on total values in DB
  return Math.ceil(productCount.value / limit.value)
})

watch(currentPage, async (newCurrentPage, oldCurrentPage) => {
  //Checks page changes to either reuse data or
  //request more from database
  let start = (newCurrentPage - 1) * limit.value
  let end = newCurrentPage * limit.value
  let len = products.value.length
  if (start >= len) {
    await loadData(len, end - len)
  }
  tableData.value = products.value.slice(start, end)
})

async function loadData(start, end) {
  //Requests data from DB
  const data = await itemsPagination(start, end)
  products.value = products.value.concat(data)
  tableData.value = products.value.slice(start, end)
}

async function getProductCount() {
  //Gets total items in database
  if (!productCount.value) {
    const res = await getCount()
    productCount.value = res.data.count
  }
}

async function setupData() {
  const data = await itemsPagination(skip.value, limit.value)
  tableData.value = data
  products.value = data
  skip.value = tableData.value.length
}

function goToDetails(item){

  adminStore.productDetails = item
  router.push("/admin/products/details")
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
          <td>{{ item['barcode'] }}</td>
          <td>{{ item.title }}</td>
          <td>{{ item.description }}</td>
          <td>{{ item.in_stock }}</td>
          <td>${{ item.price }}</td>
          <td>{{ item.sold }}</td>
          <td>
            <v-btn density="compact" @click="goToDetails(item)" class="mr-1" icon="mdi-eye"></v-btn>
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
    <div class="d-flex justify-center"></div>
  </div>
</template>
