<script setup>
import {onMounted, ref} from 'vue'
import Chart from 'chart.js/auto'
import { getTopSellers } from '../../services/orders';

const props = defineProps(['chartType', 'chartData', 'chartOptions'])
const labels = ref([])
const dataValues = ref([])
const orderData = ref()



async function setupData(){
    const res = await getTopSellers()
    const data = res.data
    for(const c in data){
      labels.value.push(data[c].title)
      dataValues.value.push(data[c].in_stock)
    }
    
}

async function chartConstructor(chartType, chartOptions) {
    await setupData()
    const chartElement = document.getElementById("top-sellers");
    const chart = new Chart(chartElement, {
    type: chartType,
    data:   {
    labels: labels.value,
    datasets: [
      {
        label: "Low Stock",
        data:  dataValues.value,
        backgroundColor: "rgba(252, 144, 3, 0.7)",
        borderColor: "#5cddff",
        lineTension: 0,
        pointBackgroundColor: "#5cddff",
      }
    ],
  },
    options: chartOptions,
  });
}

onMounted(()=>{
    chartConstructor('bar', props.chartOptions)
})
</script>
<template>
    <div>
        <canvas id="top-sellers">
          
        </canvas>
    </div>
</template>