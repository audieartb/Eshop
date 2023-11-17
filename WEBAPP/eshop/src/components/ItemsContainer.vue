<script setup>
import { ref, onMounted, watch } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useProductStore } from '@/stores/products'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import ItemCard from './ItemCard.vue'
const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
const {getFavorites} = storeToRefs(store)

const baseURL = 'http://localhost:8000/api/items'
const URL = 'http://localhost:8000/api/items?skip=0&limit=5&priceFrom=50&priceTo=600&search=you'
const page = ref(1)
const search = ref('')
const favorites = ref([])
const showFavorites = ref(false)
const itemsPerPage = ref(3)
const pageCount = ref(10)
const priceFrom = ref(null)
const priceTo = ref(null)
const table_items = ref(null)
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
  },
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

function searchItems() {
  if (search.value) {
    let lowerCaseValue = search.value.split(' ').map((i) => i.trim().toLowerCase())
    table_items.value = items.value.filter((item) =>
      lowerCaseValue.some(
        (word) =>
          item.item.toLowerCase().includes(word) || item.description.toLowerCase().includes(word)
      )
    )
  }
}

function emptySearch(){
    search.value = ''
    table_items.value = items.value
}
function filterUpdate(event) {
  if (!event) {
    table_items.value = items.value.filter((i) => {
      if (priceTo.value && priceFrom.value) {
        return i.price > priceFrom.value && i.price < priceTo.value
      } else if (priceFrom.value) {
        return i.price > priceFrom.value
      } else if (priceTo.value) {
        return i.price < priceTo.value
      }
      return i
    })
    console.log(table_items.value)
  }
}

function filterFavorites(){
  if(showFavorites){
     }else{
    table_items.value = d
  }

    
}

watch(showFavorites, async(newShowFavorites, oldShowFavorites)=>{
  if(newShowFavorites){
    table_items.value = table_items.value.filter(i =>getFavorites.value.includes(i.barcode))
  }else if( !newShowFavorites && oldShowFavorites){
    table_items.value = items.value
  }
})

async function getItems() {
  table_items.value = items.value
  return
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

onMounted(() => {
  getItems()
})
</script>

<template>
  <div class="mb-10">
    <v-row class="justify-center">
      <v-col cols="6" class="d-flex">
        <v-text-field
          class="mr-3"
          density="compact"
          variant="outlined"
          label="Search"
          v-model="search"
          append-inner-icon="mdi-close-circle-outline"
          @click:appendInner="emptySearch()"
        ></v-text-field>
        <v-btn icon="mdi-magnify" color="orange" 
          @click="searchItems()"
        class="align-self-start mt-n1"></v-btn>
      </v-col>
    </v-row>

    <v-row class="justify-center mt-0">
      <v-col class="d-flex rounded-lg filter-container pa-0" cols="8">
        <div class="w-25 d-flex align-center">
          <div class="text-h6 mt-n3">$</div>
          <v-text-field
            type="number"
            hide-spin-buttons
            class="ma-2"
            density="compact"
            variant="outlined"
            label="Price from:"
            v-model="priceFrom"
          ></v-text-field>
        </div>
        <v-text-field
          class="ma-2"
          density="compact"
          variant="outlined"
          label="Price to:"
          type="number"
          hide-spin-buttons
          v-model="priceTo"
          @update:focused="filterUpdate($event)"
        ></v-text-field>

        <v-checkbox
          class="ma-2 w-10"
          density="compact"
          label="Favorites"
          v-model="showFavorites"
          @update:modelValue="filterFavorites"
        ></v-checkbox>
      </v-col>
    </v-row>
  </div>
  <template v-if="table_items">
    <div v-if="table_items.length > 0" class="d-flex flex-wrap justify-space-between">
    <ItemCard v-for="(item, idx) in table_items" :key="idx" v-bind:item="item"></ItemCard>
    <v-pagination :length="4" v-model="page"></v-pagination>
  </div>
  <div v-else>
    <div>There's no products matching your search</div>
  </div>
  </template>
  <template v-else>
    <div>
      There's nothing here
    </div>
  </template>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
}

#filters {
  max-height: 3rem;
}
</style>
