<script setup>
import { onMounted, ref } from 'vue'
import { getTopCustomers } from '../../services/orders'

const orderData = ref([])

async function setupData() {
  const res = await getTopCustomers()

  const jsondata = JSON.parse(res.data)

  for (const c in jsondata) {
    orderData.value.push(jsondata[c])
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
          <th>Email</th>
          <th>Total Orders</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="entry in orderData">
          <td>
            {{ entry.email }}
          </td>
          <td class="centered-column">
            {{ entry.total }}
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