<script setup>
import {onMounted, ref} from 'vue'
import Chart from 'chart.js/auto'
import { getOrderByDay } from '../../services/orders';

const props = defineProps(['chartType', 'chartData', 'chartOptions'])
const labels = ref([])
const dataValues = ref([])
const orderData = ref()



async function setupData(){
    const res = await getOrderByDay()
    const jsondata = JSON.parse(res.data)
    for(const c in jsondata){
        let to_date = new Date(Number(c)).toLocaleDateString(undefined, {month: 'numeric', day: 'numeric' })
        labels.value.push(to_date)
        dataValues.value.push(jsondata[c])
    }
    
}

async function chartConstructor(chartType, chartOptions) {
    await setupData()
    const chartElement = document.getElementById("daily-count");
    const chart = new Chart(chartElement, {
    type: chartType,
    data:   {
    labels: labels.value,
    datasets: [
      {
        label: "This week",
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
        <canvas id="daily-count">
          
        </canvas>
    </div>
</template>