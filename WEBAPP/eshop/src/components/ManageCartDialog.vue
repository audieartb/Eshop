<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useProductStore } from '@/stores/products'
import { storeToRefs } from 'pinia'
import { RouterLink, useRoute, useRouter } from 'vue-router'

const store = useCartStore()
const productStore = useProductStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
const { products } = storeToRefs(productStore)

const route = useRoute()
const router = useRouter()

const dialog = ref()
const snackbar = ref(false)
const text = ref('')
const timeout = 2500
const snackbarColor = ref('')

function cartText(count) {
  return !count ? 'this cart is empty' : `You have ${count} items in this cart`
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

async function editCart(cartId) {
  if (route.params.id) {
    switchCart(cartId)
  } else {
    switchCart(cartId)
    router.push('/cart')
  }
  dialog.value = false
}

const close = () => (dialog.value = false)
const open = () => (dialog.value = true)

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
  <div>
    <v-btn @click.stop="open">Carts</v-btn>
    <v-dialog width="700" v-model="dialog">
      <v-card class="mb-3 px-2">
        <div class="d-flex justify-center my-2">
          <div class="text-h4">Manage Carts</div>
        </div>
        <v-card
          class="cart-row mb-3"
          :color="currentCart == key ? 'orange-lighten-2' : ''"
          v-for="[key, value] of Object.entries(carts)"
          :key="key"
          scrollable
        >
          <v-card-text>{{ cartText(value.total_items) }}</v-card-text>
          <v-sheet class="mx-2 rounded d-flex">
            <v-slide-group class="pa-2 items-slide" show-arrows>
              <v-slide-group-item v-for="item in value.items">
                <div class="item-small-view elevation-3">
                  <v-img
                    heigh="50"
                    class="img-icon"
                    src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
                    cover
                  >
                  </v-img>
                  <div class="text-body-1">{{ item.title }}</div>
                  <div class="text-caption">{{ item.qty }}</div>
                </div>
              </v-slide-group-item>
            </v-slide-group>
            <v-btn class="align-self-center" @click="editCart(key)">Edit</v-btn>
          </v-sheet>
          <div class="d-flex justify-center my-2">
            <v-btn class="mx-2" @click="switchCart(key)" density="comfortable">Select</v-btn>
            <v-btn class="mx-2" @click="deleteCart(key)" density="comfortable" color="red-darken-1"
              >Delete</v-btn
            >
          </div>
        </v-card>
      </v-card>
      <div class="my-2 d-flex justify-center">
        <div class="">
          <v-btn class="mb-1 w-100" @click="createNewCart">Create New Cart</v-btn>
          <v-btn class="w-100" @click="close">Done</v-btn>
        </div>
      </div>
    </v-dialog>

    <v-snackbar v-model="snackbar" :timeout="timeout" :color="snackbarColor">
      {{ text }}
      <v-btn color="blue" variant="text" @click="snackbar = false" icon="close"> </v-btn>
    </v-snackbar>
  </div>
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
