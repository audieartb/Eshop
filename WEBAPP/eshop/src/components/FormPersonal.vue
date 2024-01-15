<script setup>
import { ref, reactive } from 'vue'

import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import { useVuelidate } from '@vuelidate/core'
import { email, required, numeric, helpers } from '@vuelidate/validators'

const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)

const emit = defineEmits(['click-next', 'click-prev'])
const deliveryOpts = ['quick', 'slow', 'super slow']

const initialState = {
  name: '',
  lastname: '',
  email: '',
  verify_email: '',
  country: '',
  city: '',
  address: '',
  zip: '',
  delivery: null
}

const state = reactive({
  ...initialState
})

const isMatch = () => {
  return state.email === state.verify_email
}

const rules = {
  name: { required },
  lastname: { required },
  email: { required, email },
  verify_email: { required, email, required: helpers.withMessage('Emails must match', isMatch) },
  country: { required },
  city: { required },
  address: { required },
  zip: { required },
  delivery: { required }
}

const v$ = useVuelidate(rules, state)

function clear() {
  v$.value.$reset()
  for (const [key, value] of Object.entries(initialState)) {
    state[key] = value
  }
}

async function submit() {
  
  const result = await v$.value.$validate()
  if (result) {
    const form_data = {
      email: state.email,
      address: `${state.country}, ${state.city}, ${state.address}, ${state.zip}`,
      status: 'pending',
      total: 0,
      items: [],
      delivery_type: state.delivery,
    }
    store.form_data = form_data
    emit('click-next')
  } else {
    alert('Errors in form')
  }
}

function disablePaste(event) {
  event.preventDefault()
}
</script>

<template>
  <div class="stepper-item d-flex flex-column">
    <v-container class="column-item">
      <v-row class="justify-center">
        <div class="text-h6">Fill in to continue with payment</div>
      </v-row>
      <v-row>
        <v-col class="v-col-md-6 v-col-sm-12 v-col-xs-12">
          <v-text-field
            class="row-field"
            variant="outlined"
            v-model="state.name"
            @input="v$.name.$touch"
            @blur="v$.name.$touch"
            label="First Name"
            :error-messages="v$.name.$errors.map((e) => e.$message)"
            required
          ></v-text-field>
        </v-col>
        <v-col class="v-col-md-6 v-col-sm-12">
          <v-text-field
            class="row-field"
            variant="outlined"
            v-model="state.lastname"
            @input="v$.lastname.$touch"
            @blur="v$.lastname.$touch"
            label="Last Name"
            :error-messages="v$.lastname.$errors.map((e) => e.$message)"
            required
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col class="v-col-md-6 v-col-sm-12">
          <v-text-field
            id="email-field"
            variant="outlined"
            v-model="state.email"
            @input="v$.email.$touch"
            @blur="v$.email.$touch"
            label="Email"
            :error-messages="v$.email.$errors.map((e) => e.$message)"
            required
            autocomplete="on"
          ></v-text-field>
        </v-col>
        <v-col class="v-col-md-6 v-col-sm-12">
          <v-text-field
            id="email-field"
            variant="outlined"
            v-model="state.verify_email"
            @paste="disablePaste"
            @input="v$.verify_email.$touch"
            @blur="v$.verify_email.$touch"
            label="Verify Email"
            :error-messages="v$.verify_email.$errors.map((e) => e.$message)"
            required
            autocomplete="off"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col class="v-col-md-6 v-col-sm-12">
          <v-text-field
            class="row-field"
            variant="outlined"
            v-model="state.country"
            @input="v$.country.$touch"
            @blur="v$.country.$touch"
            label="Country"
            :error-messages="v$.country.$errors.map((e) => e.$message)"
            required
          ></v-text-field>
        </v-col>
        <v-col class="v-col-md-6 v-col-sm-12">
          <v-text-field
            class="row-field"
            variant="outlined"
            v-model="state.city"
            @input="v$.city.$touch"
            @blur="v$.city.$touch"
            label="City"
            :error-messages="v$.city.$errors.map((e) => e.$message)"
            required
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col class="v-col-md-6 v-col-sm-12">
          <v-text-field
            variant="outlined"
            v-model="state.address"
            @input="v$.address.$touch"
            @blur="v$.address.$touch"
            label="Address"
            :error-messages="v$.address.$errors.map((e) => e.$message)"
            required
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col class="v-col-md-6 v-col-sm-12">
          <v-text-field
            class="row-field"
            variant="outlined"
            v-model="state.zip"
            @input="v$.zip.$touch"
            @blur="v$.zip.$touch"
            label="Zip Code"
            :error-messages="v$.zip.$errors.map((e) => e.$message)"
            required
          ></v-text-field>
        </v-col>
        <v-col class="v-col-md-6 v-col-sm-12">
          <v-select
            variant="outlined"
            class="row-field"
            v-model="state.delivery"
            :items="deliveryOpts"
            @input="v$.delivery.$touch"
            @blur="v$.delivery.$touch"
            label="Delivery Type"
            :error-messages="v$.delivery.$errors.map((e) => e.$message)"
            required
          ></v-select>
        </v-col>
      </v-row>
    </v-container>
    <v-row class="d-flex justify-space-between column-item align-end mb-2">
      <v-col class="v-col-md-4 v-col-sm-8 justify-center">
        <v-btn class="w-50" @click="$emit('click-prev')"
          >Go Back <v-icon icon="mdi-restart"></v-icon
        ></v-btn>
      </v-col>
      <v-col class="v-col-md-4 v-col-sm-8 d-flex justify-center">
        <v-btn class="w-50" @click="clear"
          >Clear Form <v-icon icon="mdi-delete-sweep-outline"></v-icon
        ></v-btn>
      </v-col>
      <v-col class="v-col-md-4 v-col-sm-8 d-flex justify-end">
        <v-btn class="w-50" @click="submit">Submit</v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
.row-field {
  margin: 0;
}

.column-item {
  flex: 1;
}
</style>
