<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
const items = ref([
  {
    barcode: '100000000011',
    item: 'Coffee Maker',
    description: 'Programmable coffee maker with timer',
    in_stock: 15,
    price: 49.99,
    sold: 5
  },
  {
    barcode: '100000000012',
    item: 'Smart TV',
    description: '4K smart TV for your entertainment',
    in_stock: 14,
    price: 699.99,
    sold: 3
  },
  {
    barcode: '100000000013',
    item: 'Sofa',
    description: 'Comfortable sofa for your living room',
    in_stock: 25,
    price: 499.99,
    sold: 6
  }
])

async function addToCart(item) {
  await store.addToCart(item)
  console.log(store.carts[store.currentCart].items)
}

function inCart(barcode) {
  let item = store.getCountFromCart(barcode)
}

function removeFromCart(item) {
  store.removeOneFromCart(item)
}
</script>

<template>
  <div class="container">
    <v-card class="mx-auto" max-width="400" v-for="(item, index) in items" :key="index">
      <v-img
        class="align-end text-white"
        height="200"
        src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
        cover
      >
      </v-img>

      <v-card-title class="pt-4">
        {{ item.item }}
      </v-card-title>

      <v-card-text>
        <div>{{ item.description }}</div>
      </v-card-text>

      <v-card-actions class="d-flex justify-space-between">
        <v-btn w-auto color="orange"> $ {{ item.price }} </v-btn>
        <div class="d-flex align-center" v-if="carts[currentCart].items[item.barcode]">
          <v-btn color="orange" @click="removeFromCart(item)" icon="mdi-minus"></v-btn>
          <p readonly>{{ carts[currentCart].items[item.barcode].qty }}</p>
          <v-btn color="orange" @click="addToCart(item)" icon="mdi-plus"> </v-btn>
        </div>
        <v-btn v-else color="orange" @click="addToCart(item)"> Add to cart </v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <div>
    Items in Cart
    {{ carts[currentCart].items }}
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
}
</style>
