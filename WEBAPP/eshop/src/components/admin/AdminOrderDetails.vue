<script setup>
import { ref, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
const adminStore = useAdminStore()

const order = adminStore.orderDetails
</script>
<template>
  <v-card>
    <v-card-item>
      <v-row class="ma-4">
        <v-col>
          <v-card-item> <b>Created on:</b> {{ order.created_at }} </v-card-item>
          <v-card-item><b> Order Id:</b> {{ order.order_id }} </v-card-item>
          <v-card-item><b>Email:</b> {{ order.email }} </v-card-item>
          <v-card-item><b> Address:</b> {{ order.address }} </v-card-item>
        </v-col>
        <v-col>
          <v-card-item><b>Status:</b> {{ order.status }} </v-card-item>
          <v-card-item> <b>Delivery Type:</b> {{ order.delivery_type }} </v-card-item>
        </v-col>
      </v-row>
    </v-card-item>
    <v-card-item class="ma-5 elevation-2">
      <v-card-title>Order Items</v-card-title>
      <v-row v-for="item in order.items">
        <v-col cols="2">
          <p>Product</p>
          <v-card-subtitle>{{ item.title }}</v-card-subtitle>
        </v-col>
        <v-col cols="2">
          <p>Qty.</p>
          <v-card-subtitle>{{ item.qty }}</v-card-subtitle>
        </v-col>
        <v-col cols="2">
          <p>Price</p>
          <v-card-subtitle>{{ item.price }}</v-card-subtitle></v-col
        >
        <v-col>
          <p>Subtotal</p>
          <p>{{ item.price * item.qty }}</p>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-col cols="5"></v-col>
        <v-col cols="1" class="mt-4"><b>Total:</b></v-col>
        <v-col class="mt-4">
          <b> {{ order.total }}</b>
        </v-col>
      </v-row>
    </v-card-item>
  </v-card>
</template>
