<script setup>
import { RouterLink } from 'vue-router';
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
      <v-icon class="mb-5" color="success" icon="mdi-check-circle" size="112"></v-icon>

      <h2 class="text-h5 mb-6">Your order has been submitted!</h2>

      <p class="mb-4 text-medium-emphasis text-body-2">
        Check your email for order details

        <br />
        Thank you for shopping!
      </p>

      <v-divider class="mb-4"></v-divider>

      <div class="text-end">
        <v-btn class="text-none" color="orange" rounded variant="flat"> <router-link to="/">Back to Store </router-link></v-btn>
      </div>
    </v-sheet>
  </div>
</template>
