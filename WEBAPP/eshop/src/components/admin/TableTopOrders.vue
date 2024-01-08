<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getTopOrders, getOrderDetails} from '../../services/orders'
import { useAdminStore } from '../../stores/admin';
const adminStore = useAdminStore()
const router = useRouter()
const orderData = ref([])

async function setupData() {
  const res = await getTopOrders()

  const jsondata = JSON.parse(res.data)
  orderData.value = jsondata
  return
}

async function goToDetails(order) {
  console.log(order)
  if (order) {
    let items = await getOrderDetails(order.order_id)
    order.items = items.data
    console.log(items)
    console.log(order)
    adminStore.orderDetails = order
    router.push({ name: 'order-details'})
  }
}

onMounted(async () => {
  await setupData()
})
</script>
<template>
  <div>
    <v-table density="compact" :hover="true">
      <thead>
        <tr>
          <th>Order Id</th>
          <th>Total Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in orderData">
          <td>
            <div @click="goToDetails(entry)">
              {{ entry.email }}
            </div>
          </td>
          <td>
            <div @click="goToDetails(entry)">
              {{ entry.total }}
            </div>
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>
<style scoped>
td{
  cursor: pointer;
}
</style>