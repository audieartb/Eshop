<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import { RouterLink } from 'vue-router'
import  ManageCartDialog from './ManageCartDialog.vue'
const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
</script>

<template>
  <div>
    <v-app-bar>
      <router-link to="/"> <div class="text-h3 ml-5">What are you buying?</div></router-link>

      <template v-slot:append>
        <v-btn icon="mdi-magnify"></v-btn>
        <v-btn icon="mdi-heart"> </v-btn>
        <v-btn v-if="carts[currentCart]" stacked id="cart-options">
          <v-badge :content="carts[currentCart].total_items" color="error">
            <v-icon>mdi-cart</v-icon>
          </v-badge>
        </v-btn>
        <v-btn v-else icon="mdi-cart" id="cart-options"></v-btn>
        <v-menu activator="#cart-options">
          <v-list>
            <v-list-item>
              <v-list-item-title><manage-cart-dialog></manage-cart-dialog></v-list-item-title>

              <v-list-item-title
                ><v-btn>
                  <router-link to="/cart">Checkout</router-link>
                </v-btn></v-list-item-title
              >
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>
  </div>
</template>

<style scoped></style>
