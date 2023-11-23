<script setup>
import { ref, reactive } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import FormPersonal from '../components/FormPersonal.vue'
import CartCheckout from '../components/CartCheckout.vue'
import FormPayment from '../components/FormPayment.vue'
const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
const {justItems} = storeToRefs(store)
const stepper = ref()
const emit  = defineEmits(['next'])
async function addToCart(item) {
  await store.addToCart(item)
  console.log(store.carts[store.currentCart].items)
}

function next(){
  if(stepper.value){
    stepper.value.next()
  }
}

function prev(){
  if(stepper.value){
    stepper.value.prev()
  }
}

function removeFromCart(item) {
  store.removeOneFromCart(item)
}
</script>

<template>
  <v-stepper hide-actions ref="stepper" :items="['Current Cart','Personal Information', 'Payment']">
    <template v-slot:item.1>
      <CartCheckout @click-next="next"></CartCheckout>
    </template>
    <template v-slot:item.2>
      <FormPersonal @click-next="next" @click-prev="prev"></FormPersonal>
    </template>
    <template v-slot:item.3>
      <FormPayment  @click-prev="prev"></FormPayment>
    </template>
  </v-stepper>

</template>
