<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useProductStore } from '@/stores/products'
import { storeToRefs } from 'pinia'
import { RouterLink } from 'vue-router'

const store = useCartStore()
const productStore = useProductStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
const { products } = storeToRefs(productStore)

const snackbar = ref(false)
const text = ref('')
const timeout = 2500
const snackbarColor = ref('')
function cartText(count){
  if(!count){
    return 'this cart is empty'
  }else{
    return `You have ${count} items in this cart`
  }
}
async function createNewCart() {
  let res = await store.createCart()
  if (!res) {
    showSnackbar('you cannot create more', 'red-accent-3')
  } else {
    showSnackbar('New cart added', 'green-darken-2')
  }
}

async function switchCart(cartId) {
  await store.setCurrentCart(cartId)
}

async function deleteCart(cartId) {
  let deleted = await store.deleteCart(cartId)
  if (deleted) {
    showSnackbar('cart has been deleted', 'orange-lighten-1')
  }
}

function showSnackbar(customText, color) {
  if (snackbar.value) {
    snackbar.value = false
  }
  text.value = customText
  snackbar.value = true
  snackbarColor.value = color
  setTimeout(() => {
    if (!snackbar.value) {
      snackbar.value = false
    }
  }, timeout)
}
</script>

<template>
  <v-dialog width="700">
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" text="Manage Carts"> </v-btn>
    </template>
    <template v-slot:default="{ isActive }">
      <v-card class="mb-3 px-2">
        <div class="d-flex justify-center my-2">
          <div class="text-h4">Manage Carts</div>
        </div>
        <v-card
          class="cart-row mb-3"
          :color="currentCart == key ? 'orange-lighten-2' : ''"
          v-for="[key, value] of Object.entries(carts)"
          :key="key"
        >
          <v-card-text>{{cartText(value.total_items)}}</v-card-text>
          <v-sheet class="mx-2 rounded d-flex" >
            <v-slide-group class="pa-2 items-slide" show-arrows>
              <v-slide-group-item v-for="item in value.items" >
                <div class="item-small-view elevation-3" >
                  <v-img
                    heigh="50"
                    class="img-icon"
                    src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
                    cover
                  >
                  </v-img>
                  <div class="text-body-1">{{ item.title }}  </div>
                  <div class="text-caption">{{ item.qty }}</div>

                </div>
              </v-slide-group-item>
            </v-slide-group>
            <v-btn class="align-self-center" @click="isActive.value = false"><router-link to="/cart">Edit</router-link></v-btn>
          </v-sheet>

          <div class="d-flex justify-center my-2">
            <v-btn class="mx-2" @click="switchCart(key)">Select</v-btn>
            <v-btn class="mx-2" @click="deleteCart(key)" color="red-darken-1">Delete</v-btn>
          </div>
        </v-card>
      </v-card>
      <div class="my-2 d-flex flex-column">
        <v-btn class="mb-1" @click="createNewCart">Create New Cart</v-btn>
        <v-btn @click="isActive.value = false">Done</v-btn>
      </div>
    </template>
  </v-dialog>

  <v-snackbar v-model="snackbar" :timeout="timeout" :color="snackbarColor">
    {{ text }}
    <v-btn color="blue" variant="text" @click="snackbar = false" icon="close"> </v-btn>
  </v-snackbar>
</template>

<style scoped>
.isCurrent {
  background-color: rgb(247, 205, 127);
}

.item-small-view {
  width: 8rem;
  padding: 0.25rem;
  margin-inline: 0.25rem;
  border: solid;
  border-radius: 5%;
  border-color: rgb(201, 207, 207);
  
  .img-icon {
    width: 100%;
  }

  .desc-small {
  }
}

.items-slide {
  width: 85%;
  height: 10rem;
}
</style>