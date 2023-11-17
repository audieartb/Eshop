<script setup>
import { ref, onMounted} from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import axios from 'axios'
import ItemCard from './ItemCard.vue'
const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)

const baseURL = 'http://localhost:8000/api/items'
const URL = 'http://localhost:8000/api/items?skip=0&limit=5&price_from=50&price_to=600&search=you'
const page = ref(1)
const skip = ref(0)
const limit = ref(0)
const search = ref('')
const favorites = ref([])
const filterFavorites = ref(false)
const itemsPerPage = ref(3)
const pageCount = ref(10)
const price_from = ref(0)
const price_to = ref(null)


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

const table_items = ref([])

const priceFilter = ()=>{
  console.log('filtering')
  table_items.value = items.value.filter((i)=>{
    if( price_to.value){
      return i.price > price_from.value && i.price < price_to.value
    }else{
      console.log(i.price)
      return i.price > price_from.value
    }
  })
  console.log(table_items.value)
}

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

onMounted(() => {

  //getItems()
})
</script>

<template>
  <div>
    <v-row class="justify-center">
      <v-col cols="2" class="">
        <div class="text-h6">Price range</div>
      </v-col>
      <v-col cols="2">
        <v-text-field density="compact" variant="outlined" label="From:"></v-text-field>
      </v-col>
      <v-col cols="2">
        <v-text-field density="compact" variant="outlined" label="To:"></v-text-field>
      </v-col>
      <v-col cols="2">
        <v-checkbox density="compact" label="Favorites" v-model="filterFavorites"></v-checkbox>
      </v-col>
      <v-col cols="3">
        <v-btn density="compact" label="Search"> Filter</v-btn>
      </v-col>
    </v-row>
  </div>
  <div class="d-flex flex-wrap justify-space-between">  
       <ItemCard v-for="(item, idx) in items" :key="idx" v-bind:item="item"></ItemCard>
      
    <v-pagination :length="4" v-model="page"></v-pagination>
  </div>
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
