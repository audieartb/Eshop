<script setup>
import { ref, reactive } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useVuelidate } from '@vuelidate/core'
import { email, required, numeric, minLength, maxLength } from '@vuelidate/validators'
import router from '../router'

const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)


const newOrder = {
  //orderId: '231108-XDBRIEKM',
  email: store.email,
  items: [],
  status: '',
  transaction_id: '',
  created_at: '',
  //cartId: currentCart,//control
  total: 0,
  address: ''

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
  number: { required, numeric, minLength: 1, maxLength: 16 },
  cvv: { required, numeric },
  exp: { required }
}

const v$ = useVuelidate(rules, formState)

function clear() {
  v$.value.$reset()
  for (const [key, value] of Object.entries(initialState)) {
    formState[key] = value
  }
}

function processItems() {
  let orderItems = []
  let justItems = store.justItems
  for(const item in justItems){
    newOrder.items.push({ barcode: justItems[item].barcode }, { qty: justItems[item].qty })
  } 
}

async function checkAvailability(){
    
}


function processPayment() {

    alert(`payment successful`)
    newOrder.total = store.carts[store.currentCart].total
    newOrder.status = 'pending'
    newOrder.paymentId = '1234'
    newOrder.date = String(Date.now())
    processItems()
    store.deleteCart(currentCart)
    return router.push({path: '/complete'})

}   

</script>

<template>
  <div>
    <form action="">
      <v-text-field label="Name on Card" :error-messages="'error'" required></v-text-field>
      <v-text-field label="Card Number" :error-messages="'error'" required></v-text-field>
      <v-text-field label="Cvv" :error-messages="'error'" required></v-text-field>
      <v-text-field label="Expiration Date" :error-messages="'error'" required></v-text-field>
      <v-btn class="me-4" @click="processPayment()" >Complete Order</v-btn>
    </form>
  </div>
</template>
