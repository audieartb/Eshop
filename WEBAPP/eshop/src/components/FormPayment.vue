<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import { useProductStore } from '@/stores/products'
import { useVuelidate } from '@vuelidate/core'
import { required, numeric, minLength, maxLength } from '@vuelidate/validators'
import router from '../router'
import { postOrder } from '../services/orders'

const store = useCartStore()
const { form_data } = storeToRefs(store)

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
  number: { required, numeric, minLength: 15, maxLength: 16 },
  cvv: { required, numeric, minLength: 3, maxLength: 3 },
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
  let justItems = []

  for (const item in store.justItems) {
    justItems.push({
      id: store.justItems[item].id,
      barcode: store.justItems[item].barcode,
      qty: store.justItems[item].qty,
      price: store.justItems[item].price,
    })
  }
  store.form_data.temp_id = ''
  store.form_data.items = justItems
}

async function processPayment() {
  form_data['total'] = store.carts[store.currentCart].total.toFixed(2)
  console.log(form_data.value)
  const res = await postOrder(form_data.value)
  if (res.status != 200) {
    alert('Error processing order')
    console.log(res)
  }
  alert(`payment successful`)
  store.deleteCart(store.currentCart)
  router.push({ path: '/complete' })
}

onMounted(() => {
  processItems()
})
</script>

<template>
  <div class="stepper-item d-flex flex-column">
    <v-row>
      <v-col class="col-6">
        <v-card>
          <v-card-title>Summary</v-card-title>

          <v-card-item>
            <v-card-text>email: {{ form_data.email }}</v-card-text>
            <v-card-text>Address: {{ form_data.address }}</v-card-text>
            <v-card-text>Delivery type: {{ form_data.delivery_type }}</v-card-text>
          </v-card-item>
          <v-card-item>
            <v-card-text v-for="item in store.carts[store.currentCart].items">
              {{ item.title }} x {{ item.qty }} : {{ item.price * item.qty }}</v-card-text
            >
          </v-card-item>
          <v-card-text>{{ store.carts[store.currentCart].total.toFixed(2) }}</v-card-text>
        </v-card>
      </v-col>
      <v-col class="col">
        <v-sheet class="column-item d-flex justify-center align-center">
          <div class="w-100">
            <form action="">
              <v-text-field label="Name on Card" :error-messages="'error'" required></v-text-field>
              <v-text-field label="Card Number" :error-messages="'error'" required></v-text-field>
              <v-text-field label="Cvv" :error-messages="'error'" required></v-text-field>
              <v-text-field
                label="Expiration Date"
                :error-messages="'error'"
                required
              ></v-text-field>
            </form>
          </div>
        </v-sheet>
      </v-col>
    </v-row>

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
