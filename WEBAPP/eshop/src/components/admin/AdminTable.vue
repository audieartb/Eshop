<script setup>
import { ref, onMounted, computed, watch, defineEmits, defineProps } from 'vue'
import { getCount, itemsPagination } from '../../services/items'
import {useAdminStore} from '../../stores/admin'
import router from '../../router';
import { all } from 'axios';
const emit = defineEmits(['getData'])
const props = defineProps(['columns'])

const adminStore = useAdminStore()

const limit = ref(5)
const skip = ref(0)
const tableData = ref([])
const allData = ref([])
const dataCount = ref(null)
const currentPage = ref()

const pages = computed(() => {
  console.log('computed', dataCount.value)
  return Math.ceil(dataCount.value / limit.value)
})

watch(currentPage, async (newCurrentPage, oldCurrentPage) => {
  let start = (newCurrentPage - 1) * limit.value
  let end = newCurrentPage * limit.value
  let len = allData.value.length
  if (start >= len) {
    await loadData(len, end - len)
  }
  tableData.value = allData.value.slice(start, end)
})

async function loadData(start, end) {
  const data = await itemsPagination(start, end)
  allData.value = allData.value.concat(data)
  tableData.value = allData.value.slice(start, end)
}

async function getdataCount() {
  if (!dataCount.value) {
    const res = await getCount()
    dataCount.value = res.data.count
  }
}



async function setupData() {
  const data = await itemsPagination(skip.value, limit.value)
  tableData.value = data
  allData.value = data
  skip.value = tableData.value.length
  console.log(allData.value)
}

function goToDetails(item){

  adminStore.productDetails = item
  router.push("/admin/products/details")
}

onMounted(() => {
  getdataCount()
  setupData()
})
</script>
<template>
  <div class="ml-4">
    <v-table fixed-header>
      <thead>
        <tr>
          <th class="text-left" v-for="col in props.columns">{{ col.name }}</th>
          <th class="text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in tableData" :key="item.id">
          <td v-for="col in props.columns">{{ item[col.key] }}</td>
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
