<script setup>
import { ref, reactive } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useOrderStore } from '@/stores/orders'
import { storeToRefs } from 'pinia'

import { useVuelidate } from '@vuelidate/core'
import { email, required, numeric, minLength, maxLength } from '@vuelidate/validators'

const store = useCartStore()
const { justItems } = storeToRefs(store)
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)

var total = carts
console.log(total)

const newOrder = {
  orderId: '',
  email: store.email,
  items: [],
  status: '',
  paymentId: '',
  date: '',
  cartId: currentCart,
  total: 0,
}

const initialState = {
  name: '',
  number: '',
  cvv: '',
  exp: ''
}
const formState = reactive({
  ...initialState
})

const rules = {
  name: { required },
  number: { required, numeric, minLength: 16, maxLength: 16 },
  cvv: { required, numeric },
  exp: { required }
}
function clear() {
  v$.value.$reset()
  for (const [key, value] of Object.entries(initialState)) {
    state[key] = value
  }
}

function processItems() {
  const orderItems = []
  justItems.forEach((item) => {
    orderItems.push({ barcode: item.barcode }, { qty: item.qty })
  })
}

async function checkAvailability(){
    
}


function processPayment(card) {

    newOrder.status = 'pending',
    newOrder.paymentId = '1234',
    newOrder.date = String(Date.now())
    alert('payment successful')
    clear()
}   

</script>

<template>
  <div>
    <form action="">
      <v-text-field label="Name on Card" :error-messages="'error'" required></v-text-field>
      <v-text-field label="Card Number" :error-messages="'error'" required></v-text-field>
      <v-text-field label="Cvv" :error-messages="'error'" required></v-text-field>
      <v-text-field label="Expiration Date" :error-messages="'error'" required></v-text-field>
      <v-btn class="me-4">Complete Order</v-btn>
    </form>
  </div>
</template>
