<script setup>
import Navigation from '../../components/admin/Navigation.vue'
import OrdersMonth from '../../components/admin/OrdersMonth.vue'
import OrderDailyCount from '../../components/admin/OrderDailyCount.vue'
import ChartTopEmails from '../../components/admin/ChartTopEmails.vue'
import TableTopOrders from '../../components/admin/TableTopOrders.vue'
</script>

<template>
  <div class="admin-data-container">

    <v-row class="flex-nowrap">
      <v-col cols="6" class="">
        <div>No. of Orders by Month</div>
        <OrdersMonth></OrdersMonth>
      </v-col>
      <v-col cols="6" class="">
        <div>No. Orders in the last 30 days</div>
        <OrderDailyCount></OrderDailyCount>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6" class=" ">
        <div>Customer with the Most Orders</div>
        <ChartTopEmails></ChartTopEmails>
      </v-col>
      <v-col cols="6" class=" ">
        <div>Highest Orders of all time </div>
        <TableTopOrders></TableTopOrders>
      </v-col>
    </v-row>
  </div>
</template>
<style scoped>
.admin-data-container {
  height: 100%;
}
</style>
