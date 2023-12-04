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
  address: '',
  transaction_id: '',
  status: '',
  total: 0,
  items: []
  //cartId: currentCart,//control
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
  for (const item in justItems) {
    newOrder.items.push({ barcode: justItems[item].barcode }, { qty: justItems[item].qty })
  }
}

async function checkAvailability() {}

function processPayment() {
  alert(`payment successful`)
  newOrder.total = store.carts[store.currentCart].total
  newOrder.status = 'pending'
  newOrder.paymentId = '1234'
  newOrder.date = String(Date.now())
  processItems()
  store.deleteCart(currentCart)
  return router.push({ path: '/complete' })
}
</script>

<template>
  <div class="stepper-item d-flex flex-column">
    <v-sheet class="column-item d-flex justify-center align-center">
      <div class="w-50">
        <form action="">
          <v-text-field label="Name on Card" :error-messages="'error'" required></v-text-field>
          <v-text-field label="Card Number" :error-messages="'error'" required></v-text-field>
          <v-text-field label="Cvv" :error-messages="'error'" required></v-text-field>
          <v-text-field label="Expiration Date" :error-messages="'error'" required></v-text-field>
        </form>
      </div>
    </v-sheet>
    <v-row class="d-flex justify-space-between column-item align-end mb-2">
      <v-col class="v-col-md-4 v-col-sm-8 justify-center">
        <v-btn class="w-50" @click="$emit('click-prev')">Go Back</v-btn>
      </v-col>
      <v-col class="v-col-md-4 v-col-sm-8 d-flex justify-end">
        <v-btn class="me-4 w-50" @click="processPayment()">Complete Order</v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
.column-item {
  flex: 1;
}
</style>
