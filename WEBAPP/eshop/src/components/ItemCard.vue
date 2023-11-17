<script setup>

import { ref, defineProps } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import { RouterLink } from 'vue-router'

const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
const {getFavorites} = storeToRefs(store)
const props = defineProps(['item'])


function removeFromCart(item) {
  store.removeOneFromCart(item)
}
async function addToCart(item) {
  await store.addToCart(item)
  console.log(store.carts[store.currentCart].items)
}
function inCart(barcode) {
  try {
    let item = carts[currentCart].items[barcode]
    console.log(item)
    if (item) {
      return true
    }
  } catch (error) {}
}


function isFavorite(barcode) {
  
  if (getFavorites.value.includes(barcode)) {
    return 'orange'
  } else {
    return 'black'
  }
}

function addToFavorites(barcode) {
  console.log(barcode)
  let idx = getFavorites.value.indexOf(barcode)
  if (idx < 0) {
    getFavorites.value.push(barcode)
  } else {
    getFavorites.value.splice(idx, 1)
  }
 
}

</script>

<template>
    <v-card class="mx-auto mb-5" max-width="400">
      <v-img
        class="align-end text-white"
        height="200"
        src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
        cover
      >
      </v-img>

      <v-card-title class="pt-4">
        {{ props.item.item }}
        <v-btn class="float-end"
          :id="'btn-' + props.item.barcode"
          icon="mdi-heart"
          variant="plain"
          size="small"
          density="compact"
          :color="isFavorite(props.item.barcode)"
          @click="addToFavorites(props.item.barcode)"
        ></v-btn>
      </v-card-title>

      <v-card-text>
        <div>{{ props.item.description }}</div>
      </v-card-text>

      <v-card-actions class="d-flex justify-space-between">
        <v-btn w-auto color="orange"> $ {{ props.item.price }} </v-btn>

        <template v-if="carts[currentCart]">
          <div class="d-flex align-center" v-if="carts[currentCart].items[props.item.barcode]">
            <v-btn color="orange" @click="removeFromCart(props.item)" icon="mdi-minus"></v-btn>
            <p readonly>{{ carts[currentCart].items[props.item.barcode].qty }}</p>
            <v-btn color="orange" @click="addToCart(props.item)" icon="mdi-plus"> </v-btn>
          </div>

          <v-btn v-else color="orange" @click="addToCart(props.item)"> Add to cart </v-btn>
        </template>
        <v-btn v-else color="orange" @click="addToCart(props.item)"> Add to cart </v-btn>
      </v-card-actions>
    </v-card>     

    
</template>