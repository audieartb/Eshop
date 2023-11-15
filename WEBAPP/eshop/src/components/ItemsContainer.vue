<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import { url } from '@vuelidate/validators'
const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)

const baseURL = 'http://localhost:8000/api/items'
const URL = 'http://localhost:8000/api/items?skip=0&limit=5&price_from=50&price_to=600&search=you'
const page = ref('')
const skip = ref('')
const limit = ref('')

const favorites = ref([])
const filterFavorites = ref(false)

const items = ref([
  {
    barcode: '100000000011',
    item: 'Coffee Maker',
    description: 'Programmable coffee maker with timer',
    in_stock: 15,
    price: 49.99,
    sold: 5
  },
  {
    barcode: '100000000012',
    item: 'Smart TV',
    description: '4K smart TV for your entertainment',
    in_stock: 14,
    price: 699.99,
    sold: 3
  },
  {
    barcode: '100000000013',
    item: 'Sofa',
    description: 'Comfortable sofa for your living room',
    in_stock: 25,
    price: 499.99,
    sold: 6
  },
  {
    barcode: '100000000014',
    item: 'Gaming Chair',
    description: 'Comfortable gaming chair for gamers',
    in_stock: 19,
    price: 159.99,
    sold: 6
  }
])


async function getItems() {
  axios
    .get(baseURL)
    .then((res) => {
      console.log(res)
      if (!items.value) {
        items.value = res.data
      } else {
        items.value.push(res.data)
      }
    })
    .catch((error) => {
      console.log(error)
    })
}



function addToFavorites(barcode) {
  console.log(barcode)
  let idx = favorites.value.indexOf(barcode)
  if(idx<0){
    favorites.value.push(barcode)
  }else{
    favorites.value.splice(idx,1)
  }
  console.log(favorites.value)
}

function isFavorite(barcode){
  if(favorites.value.includes(barcode)){
    return 'orange'
  }else{
    return 'black'
  }
}
///CART MANAGEMENT///
async function addToCart(item) {
  await store.addToCart(item)
  console.log(store.carts[store.currentCart].items)
}


function inCart(barcode) {
  try {
    let item = carts[currentCart].items[barcode]
    console.log(item)
    if (item) {
      return true
    }
  } catch (error) {}
}

function removeFromCart(item) {
  store.removeOneFromCart(item)
}


onMounted(() => {
  //getItems()
})


</script>

<template>
  <div >
      <v-row class="justify-center">
        <v-col cols="2" class="">
          <div class="text-h6">Price range</div>
        </v-col>
        <v-col cols="2">
          <v-text-field density="compact" variant="outlined"  label="From:"></v-text-field>
        </v-col>
        <v-col cols="2">
          <v-text-field density="compact" variant="outlined"  label="To:"></v-text-field>
        </v-col>
        <v-col cols="2">
          <v-checkbox density="compact" label="Favorites" v-model="filterFavorites"></v-checkbox>
        </v-col>
        <v-col cols="3">
          <v-btn density="compact" label="Search"  > Search</v-btn>
        </v-col>
      </v-row>
  </div>
  <div class="d-flex flex-wrap justify-space-between">
    <v-card class="mx-auto mb-5" max-width="400" v-for="(item, index) in items" :key="index">
      <v-img
        class="align-end text-white"
        height="200"
        src="https://cdn.vuetifyjs.com/images/cards/docks.jpg"
        cover
      >
      </v-img>

      <v-card-title class="pt-4">
        {{ item.item }}
        <v-btn class="float-end"
          :id="'btn-' + item.barcode"
          icon="mdi-heart"
          variant="plain"
          size="small"
          density="compact"
          :color="isFavorite(item.barcode)"
          @click="addToFavorites(item.barcode)"
        ></v-btn>
      </v-card-title>

      <v-card-text>
        <div>{{ item.description }}</div>
      </v-card-text>

      <v-card-actions class="d-flex justify-space-between">
        <v-btn w-auto color="orange"> $ {{ item.price }} </v-btn>

        <template v-if="carts[currentCart]">
          <div class="d-flex align-center" v-if="carts[currentCart].items[item.barcode]">
            <v-btn color="orange" @click="removeFromCart(item)" icon="mdi-minus"></v-btn>
            <p readonly>{{ carts[currentCart].items[item.barcode].qty }}</p>
            <v-btn color="orange" @click="addToCart(item)" icon="mdi-plus"> </v-btn>
          </div>

          <v-btn v-else color="orange" @click="addToCart(item)"> Add to cart </v-btn>
        </template>
        <v-btn v-else color="orange" @click="addToCart(item)"> Add to cart </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
}

#filters{
  max-height: 3rem;
}
</style>

