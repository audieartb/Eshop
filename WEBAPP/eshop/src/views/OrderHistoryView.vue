<script setup>
import { ref, reactive } from 'vue'

import { useVuelidate } from '@vuelidate/core'
import { email, required } from '@vuelidate/validators'
import { RouterLink } from 'vue-router'
import {orderHistory} from '../services/orders'

const waiting = ref(false )
const success = ref(false)
const initialState = {
  email: ''
}

const state = reactive({
  ...initialState
})

const rules = {
  email: { required, email }
}

const v$ = useVuelidate(rules, state)

async function submit() {
  const result = await v$.value.$validate()
  if (result) {
    waiting.value = true
    const res = await orderHistory(state.email)
    if(res.status == 200){
        success.value = true
        
    }else{
        alert('Error requesting order, please try again')
    }
    waiting.value = false
  }
}
</script>

<template>
  <div class="d-flex justify-center align-center">
    <v-sheet
      elevation="12"
      max-width="600"
      rounded="lg"
      width="100%"
      class="pa-4 text-center mx-auto"
    >
      <h2 class="text-h5 mb-6">Enter your email to recieve your order history</h2>
      <v-text-field
        id="email-field"
        variant="outlined"
        v-model="state.email"
        required
        autocomplete="on"
        @input="v$.email.$touch"
        @blur="v$.email.$touch"
        :disabled="waiting"
        label="Email"
        :error-messages="v$.email.$errors.map((e) => e.$message)"
      ></v-text-field>
      <v-divider class="mb-4"></v-divider>

      <div class="text-end">
        <v-btn v-if="!success" class="text-none mr-3" color="orange"  variant="flat">
          <router-link to="/">Back to Store </router-link></v-btn
        >
        <v-btn v-if="!success" color="orange" variant="flat" :disabled="waiting" @click="submit">Submit</v-btn>
        <v-btn v-else class="text-none" color="orange"  variant="flat">
          <router-link to="/">Back to Store </router-link></v-btn
        >
        
      </div>
    </v-sheet>
  </div>
  <div class="text-center loading-screen" >
    <v-progress-circular class="spinner"
    v-if="waiting"
      indeterminate
      color="primary"
      size="70"
      width="10"
    ></v-progress-circular>

  </div>
</template>

<style scoped>

.spinner{
    margin-top: 4rem;
}

</style>