<script setup>
import OrdersMonth from '../../components/admin/OrdersMonth.vue'
import OrderDailyCount from '../../components/admin/OrderDailyCount.vue'
import ChartTopEmails from '../../components/admin/ChartTopEmails.vue'
import TableTopOrders from '../../components/admin/TableTopOrders.vue'
import TopSellers from '../../components/admin/TopSellers.vue'

</script>

<template>
  <div class="admin-data-container">

    <v-row class="flex-nowrap dashboard-row">
      <v-col cols="12" class="elevation-2 dashboard-col-large" id="one-year-chart">
        <div class="center-dash-title">No. of Orders by Month</div>
        <OrdersMonth></OrdersMonth>
      </v-col>
    </v-row>
    <v-row class="flex-nowrap d-flex dashboard-row" justify="space-between">
      <v-col  class="elevation-2 dashboard-col">
        <div class="center-dash-title">Low Stock less than 10</div>
        <TopSellers></TopSellers>
      </v-col>
      <v-col  class="elevation-2 dashboard-col">
        <div class="center-dash-title">No. Orders in the last 30 days</div>
        <OrderDailyCount></OrderDailyCount>
      </v-col>
    </v-row>
    <v-row class="dashboard-row" justify="space-between">
      <v-col cols="6" class="elevation-2 dashboard-col">
        <div class="center-dash-title">Customer with the Most Orders</div>
        <ChartTopEmails></ChartTopEmails>
      </v-col>
      <v-col cols="6" class="elevation-2 dashboard-col">
        <div class="center-dash-title">Highest Orders of all time </div>
        <TableTopOrders></TableTopOrders>
      </v-col>
    </v-row>
    
  </div>
</template>
<style scoped>
.admin-data-container {
  height: 100%;
}
.center-dash-title{
  text-align: center;
  font-weight: bold;
  font-size: large;
}
.dashboard-row{
  align-items: center;
  width: 100%;
}

.dashboard-col-large{

  margin-bottom: 1rem;
}
.dashboard-col{
  max-width: 49%;
  margin-bottom: 1rem;
}
</style>
