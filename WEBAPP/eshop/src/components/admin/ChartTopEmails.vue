<script setup>
import { onMounted, ref } from 'vue'
import { getTopCustomers } from '../../services/orders'

const orderData = ref([])

async function setupData() {
  const res = await getTopCustomers()

  const jsondata = JSON.parse(res.data)

  for (const c in jsondata) {
    orderData.value.push({ x: c, y: jsondata[c] })
  }
}

onMounted(async () => {
  await setupData()
})
</script>
<template>
  <div>
    <v-table density="compact">
      <thead>
        <tr>
          <th>Email</th>
          <th>Total Orders</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in orderData">
          <td>
            {{ entry.x }}
          </td>
          <td>
            {{ entry.y }}
          </td>
        </tr>
      </tbody>
    </v-table>
  </div>
</template>
