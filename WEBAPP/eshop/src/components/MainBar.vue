<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import { RouterLink, useRouter } from 'vue-router'
import ManageCartDialog from './ManageCartDialog.vue'
import { useAdminStore } from '../stores/admin'
const adminStore = useAdminStore()
const router = useRouter()
const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)

function logout(){
  adminStore.email = ''
  adminStore.auth_token = ''
  adminStore.orderDetails = {}
  adminStore.is_authenticated = false
  router.push('/')
}

</script>

<template>
  <div>
    <v-app-bar>
      <div><router-link to="/"> <div class="text-h4 ml-5 store-title">What are you buying?</div></router-link></div>
      <div v-if="adminStore.is_authenticated" class="ml-5">
        <div class="text-h8 rounded-sm admin-msg px-2" >Logged in as admin</div>
      </div>
      <template v-slot:append>
        <v-btn v-if="adminStore.is_authenticated" @click="logout" >log out</v-btn>
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
                ><v-btn class="menu-btn">
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
<style scoped>
.admin-msg{
  color: aliceblue;
  background-color: red;
  font-weight: 500;
}
</style>