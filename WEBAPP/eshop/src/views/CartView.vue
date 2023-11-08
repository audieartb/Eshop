<script setup>
import { ref, reactive } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import FormPersonal from '../components/FormPersonal.vue'

const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
const {justItems} = storeToRefs(store)


async function addToCart(item) {
  await store.addToCart(item)
  console.log(store.carts[store.currentCart].items)
}


function removeFromCart(item) {
  store.removeOneFromCart(item)
}
</script>

<template>
  <div class="d-flex flex-wrap justify-space-between">
    <template v-if="carts[currentCart]">
      <div class="">
        <div class="d-flex align-start flex-column pt-5 v-col-sm-12">
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
                <v-text>{{ carts[currentCart].items[item.barcode].qty }}</v-text>
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
        <div class="d-flex align-end flex-column">
          <div class="text-h6">Total ${{(Math.round(carts[currentCart].total * 100) / 100).toFixed(2)  }}</div>
        </div>
      </div>
    </template>

    <div class="w-50 ma-auto">
      <FormPersonal></FormPersonal>
    </div>
  </div>
</template>
