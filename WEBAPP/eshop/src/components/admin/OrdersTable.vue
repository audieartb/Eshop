<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { getOrders, getOrderDetails, getOrderCount } from '../../services/orders'
import { useAdminStore } from '../../stores/admin'
import router from '../../router'
const adminStore = useAdminStore()
//const orders = ref({})

const limit = ref(5)
const skip = ref(0)
const tableData = ref([])
const orders = ref([])
const productCount = ref(null)
const currentPage = ref()
const showPagination = ref(true)
const filters = ref({
  email: null,
  order_id: null,
  from_date: '',
  to_date: '',
  limit: 5,
  skip: 0,
  order_by: 'created_at',
  order_asc: false
})

const pages = computed(() => {
  //Calculates how many pages based on total values in DB
  return Math.ceil(productCount.value / limit.value)
})

watch(currentPage, async (newCurrentPage, oldCurrentPage) => {
  //Checks page changes to either reuse data or
  //request more from database
  let start = (newCurrentPage - 1) * limit.value
  let end = newCurrentPage * limit.value
  let len = orders.value.length

  if (start >= len) {
    await loadData(len, end - len)
  }
  tableData.value = orders.value.slice(start, end)
})

async function loadData(start, end) {
  //Requests data from DB
  filters.value.limit = end
  filters.value.skip = start
  const data = await getOrders(filters.value)
  orders.value = orders.value.concat(data.data)
  tableData.value = orders.value.slice(start, end)
}

async function getOrdersCount() {
  //Gets total items in database
  if (!productCount.value) {
    const res = await getOrderCount()
    productCount.value = res.data.count
  }
}

async function setupData() {
  filters.value.limit = limit.value
  filters.value.skip = skip.value
  const data = await getOrders(filters.value)
  tableData.value = data.data
  orders.value = data.data
  skip.value = tableData.value.length
}

async function goToDetails(order) {
  let items = await getOrderDetails(order.order_id)
  order.items = items.data
  adminStore.orderDetails = order
  router.push({ name: 'order-details' })
}


async function searchFilter(){
  filters.value.limit = null
  filters.value.skip = 0
  const res = await getOrders(filters.value)
  tableData.value = res.data
  showPagination.value = false
}

function clearSearch(){
  currentPage.value = 1
  showPagination.value = true
  filters.value.email = null
  filters.value.order_id = null
}
onMounted(() => {
  getOrdersCount()
  setupData()
})
</script>
<template>
  <div>
    <div>
      <div>Filters</div>
      <div class="d-flex flex-wrap w-75 align-center">
        <v-text-field variant="outlined" label="Email" v-model="filters.email" class="ma-2"></v-text-field>

        <v-text-field variant="outlined" label="Order Id" v-model="filters.order_id" class="ma-2"
          ></v-text-field>
          <v-btn color="orange" class="filter-btn" @click="searchFilter">Search</v-btn>
          <v-btn color="orange" class=" filter-btn" @click="clearSearch">Clear</v-btn>
      </div>
    </div>
    <v-table>
      <thead>
        <tr>
          <th class="text-left">Order Id</th>
          <th class="text-left">Email</th>
          <th class="text-left">Status</th>
          <th class="text-left">Total</th>
          <th class="text-left">Created on</th>
          <th class="text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in tableData">
          <td>{{ order.order_id }}</td>
          <td>{{ order.email }}</td>
          <td>{{ order.status }}</td>
          <td>{{ order.total }}</td>
          <td>{{ order.created_at }}</td>
          <td>
            <v-btn
              @click="goToDetails(order)"
              density="compact"
              class="mr-1"
              icon="mdi-eye"
            ></v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    <div class="d-flex justify-center" v-if="showPagination">
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
<style scoped>

.filter-btn{
  margin: 1rem;
  width: 7rem;
}
</style>