<script setup>
import { ref , onMounted} from 'vue'
import { useAdminStore } from '../../stores/admin';
const adminStore = useAdminStore()


const order = adminStore.orderDetails


</script>
<template>
  <v-card>
    <v-card-item>
      <v-card-title> Order Details </v-card-title>
      <v-card-text> {{ order.email }} </v-card-text>
      <v-card-text> {{ order.address }} </v-card-text>
      <v-card-text> {{ order.status }} </v-card-text>
      <v-card-text> {{ order.delivery_type }} </v-card-text>
      <v-card-text> {{ order.created_at }} </v-card-text>
      <v-card-text> {{ order.order_id }} </v-card-text>
    </v-card-item>
    <v-card-item>
      <div v-for="item in order.items">
        <v-card-subtitle>{{ item.title }}</v-card-subtitle>
        <v-card-subtitle>{{ item.qty }}</v-card-subtitle>
        <v-card-subtitle>{{ item.price }}</v-card-subtitle>
      </div>
    </v-card-item>
  </v-card>
</template>
