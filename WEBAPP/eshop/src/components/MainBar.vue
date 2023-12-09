<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import { RouterLink, useRouter } from 'vue-router'
import ManageCartDialog from './ManageCartDialog.vue'
const router = useRouter()
const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
</script>

<template>
  <div>
    <v-app-bar>
      <div><router-link to="/"> <div class="text-h4 ml-5 store-title">What are you buying?</div></router-link></div>
      <template v-slot:append>
        <v-tooltip text="Order History">
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" icon="mdi-receipt" @click="router.push('/order/history')">
            </v-btn>
          </template>
        </v-tooltip>
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