<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
const adminStore = useAdminStore()

const order = adminStore.orderDetails
</script>
<template>
  <v-card>
    <v-card-item>
      <v-card-title>Order Details </v-card-title>
      <v-row>
        <v-card-item> Order Id: {{ order.order_id }} </v-card-item>
        <v-card-item>Email: {{ order.email }} </v-card-item>
        <v-card-item> Address: {{ order.address }} </v-card-item>
        <v-card-item>Status: {{ order.status }} </v-card-item>
        <v-card-item> Delivery Type: {{ order.delivery_type }} </v-card-item>
        <v-card-item> Created on: {{ order.created_at }} </v-card-item>
      </v-row>
    </v-card-item>
    <v-card-item>
      <v-card-title>Order Items</v-card-title>
      <div v-for="item in order.items">
        <v-card-subtitle>{{ item.title }}</v-card-subtitle>
        <v-card-subtitle>{{ item.qty }}</v-card-subtitle>
        <v-card-subtitle>{{ item.price }}</v-card-subtitle>
      </div>
    </v-card-item>
  </v-card>
</template>
