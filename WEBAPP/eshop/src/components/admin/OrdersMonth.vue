<script setup>
import { onMounted, ref } from 'vue'
import Chart from 'chart.js/auto'
import { getMonthlySales } from '../../services/orders'

const props = defineProps(['chartType', 'chartData', 'chartOptions'])
const orderData = ref([])

const labels = ref([])
const dataValues = ref([])

async function setupData() {
  const res = await getMonthlySales()
  const jsondata = JSON.parse(res.data)

  for (const c in jsondata) {
    orderData.value.push({ x: c, y: jsondata[c] })
  }
}

function chartConstructor(chartType, chartOptions) {
  labels.value = orderData.value.map((item) => item.x)
  dataValues.value = orderData.value.map((item) => item.y)
  const chartElement = document.getElementById('monthly-orders')
  const chart = new Chart(chartElement, {
    type: chartType,
    data: {
      labels: labels.value,
      datasets: [
        {
          label: 'Montlhy Sales',
          data: dataValues.value,
          backgroundColor: 'rgba(252, 144, 3, 0.7)',
          borderColor: '#5cddff',
          lineTension: 0,
          pointBackgroundColor: '#5cddff'
        }
      ]
    }
  })
}

onMounted(async () => {
  await setupData()
  chartConstructor('bar', props.chartOptions)
})
</script>
<template>
  <div>
    <canvas id="monthly-orders"> </canvas>
  </div>
</template>
