<script setup>
import {onMounted} from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps(['chartType', 'chartData', 'chartOptions'])

const data = {
    labels: ["Jan1", "Jan2", "Jan3", "Jan4", "Jan5", "Jan6", "Jan7"],
    datasets: [
      {
        label: "This week",
        data:  [12, 19, 10, 17, 6, 3, 7],
        backgroundColor: "rgba(224, 248, 255, 0.4)",
        borderColor: "#5cddff",
        lineTension: 0,
        pointBackgroundColor: "#5cddff",
      },
      {
        label: "Last week",
        data:  [10, 25, 3, 25, 17, 4, 9],
        backgroundColor: "rgba(241, 225, 197, 0.4)",
        borderColor: "#ffc764",
        lineTension: 0,
        pointBackgroundColor: "#ffc764",
      },
    ],
  }

function chartConstructor(chartType, chartData, chartOptions) {
    const chartElement = document.querySelector("canvas");
    const chart = new Chart(chartElement, {
    type: chartType,
    data: chartData,
    options: chartOptions,
  });
}

onMounted(()=>{
    chartConstructor('line', data, props.chartOptions)
})
</script>
<template>
    <div>
        <canvas>

        </canvas>
    </div>
</template>