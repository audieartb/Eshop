<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import { RouterLink } from 'vue-router'

const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
</script>

<template>
  <div>
    <v-app-bar>
      <div class="text-h3 ml-5">Welcome</div>
      <template v-slot:append>
        <v-btn icon="mdi-magnify"></v-btn>

        <!-- <v-btn icon="mdi-cart"></v-btn> -->
        <v-btn v-if="carts[currentCart]" stacked>
          <router-link to="/cart">
            <v-badge :content="carts[currentCart].total_items" color="error">
            <v-icon>mdi-cart</v-icon>
          </v-badge>
          </router-link>
        
        </v-btn>
        <v-btn v-else icon="mdi-cart"></v-btn>
      </template>
    </v-app-bar>
  </div>
</template>

<style scoped></style>
