<script setup>
import { ref, onMounted } from 'vue'
import { getLastDay, getOrderDetails } from '../../services/orders'
import { useAdminStore } from '../../stores/admin'
import router from '../../router'

const adminStore = useAdminStore()
const tableData = ref([])

async function setUp() {
  let data = await getLastDay()
  tableData.value = JSON.parse(data.data)
}

async function goToDetails(order) {
  let items = await getOrderDetails(order.order_id)
  order.items = items.data
  adminStore.orderDetails = order
  router.push({ name: 'order-details' })
}
onMounted(() => {
  setUp()
})
</script>

<template>
  <div>
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
  </div>
</template>
