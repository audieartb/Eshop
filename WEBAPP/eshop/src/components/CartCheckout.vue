<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'


const emit = defineEmits(['click-next', 'click-prev'])
const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
const { justItems } = storeToRefs(store)
const cartRef = ref()

async function addToCart(item) {
  await store.addToCart(item)
}


function removeFromCart(item) {
  store.removeOneFromCart(item)
}
</script>

<template>
  <div v-if="carts[currentCart]" class="stepper-item" ref="cartRef">
    <div class="d-flex flex-column">
      {{ cartPath }}
      <div class="d-flex align-start flex-column pt-5 v-col-sm-12 column-item">
        <v-card v-for="(item, idx) in carts[currentCart].items" width="400" class="mb-5 d-flex">
          <v-card-item class="align-content-start me-auto">
            <v-card-title>
              {{ item.title }}
            </v-card-title>
            <v-card-text class="pl-0"> Price: {{ item.price }} </v-card-text>
            <v-card-text class="pa-0">
              {{ item.qty }} items in cart: {{ item.qty * item.price }}</v-card-text
            >
          </v-card-item>
          <v-card-item class="d-flex flex-column" height="100%">
            <div class="alig-self-start">
              <v-btn
                @click="addToCart(item)"
                color="orange"
                size="x-small"
                variant="outlined"
                icon="mdi-plus"
              ></v-btn>
            </div>
            <div>
              <div>{{ carts[currentCart].items[item.barcode].qty }}</div>
            </div>
            <div class="align-self-end">
              <v-btn
                @click="removeFromCart(item)"
                color="orange"
                size="x-small"
                variant="outlined"
                icon="mdi-minus"
              ></v-btn>
            </div>
          </v-card-item>
          <v-card-item class="pa-0">
            <v-img
              height="125"
              width="125"
              class=""
              src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
              cover
            >
            </v-img>
          </v-card-item>
        </v-card>
      </div>
      <div class="d-flex align-end flex-column column-item">
        <div class="text-h6">
          Total ${{ (Math.round(carts[currentCart].total * 100) / 100).toFixed(2) }}
        </div>
      </div>
    </div>

  <div class=" column-item mb-2 align-end">
    <v-row class="justify-end ma-1 d-flex column-item mb-2">
      <v-col class="v-col-md-4 v-col-sm-8 d-flex justify-end">
        <v-btn class="w-50" @click="$emit('click-next')">Start Checkout</v-btn>
      </v-col>
    </v-row>
  </div>
  </div>
</template>
<style scoped>
.column-item {
  flex: 1;
}
</style>
