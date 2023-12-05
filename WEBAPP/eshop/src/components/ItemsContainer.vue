<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useProductStore } from '@/stores/products'
import { storeToRefs } from 'pinia'
import { getItems } from '../services/items'
import ItemCard from './ItemCard.vue'

const store = useCartStore()
const productsStore = useProductStore()
const { getFavorites } = storeToRefs(store)
const search = ref('')
const showFavorites = ref(false)

const pagination = ref({
  pageCount: 7,
  itemsPerPage: 9,
  start: 0,
  end: 0,
  pageIdx: 1
})

const isFiltered = ref(false)
const currentPage = ref()
const priceFrom = ref(null)
const priceTo = ref(null)
const tableItems = ref(null)
const pageItems = ref([])
const items = ref([])


// Pagination Control
function initPage() {
  items.value = productsStore.products
  if (items.value) {
    tableItems.value = items.value
    if (items.value.length < pagination.value.itemsPerPage) {
      pageItems.value = items.value
    } else {
      pageItems.value = tableItems.value.slice(0, pagination.value.itemsPerPage)
    
      pagination.value.end = pageItems.value.length - 1
    }
  }
}
function refreshPagination() {
  if (tableItems.value.length < pagination.value.itemsPerPage) {
    pageItems.value = tableItems.value
  } else {
    pageItems.value = tableItems.value.slice(0, pagination.value.itemsPerPage)
    pagination.value.end = pageItems.value.length - 1
  }
}

watch(currentPage, (newCurrentPage, oldCurrentPage) => {
  let start = (newCurrentPage - 1) * pagination.value.itemsPerPage
  let end = newCurrentPage * pagination.value.itemsPerPage

  pageItems.value = tableItems.value.slice(start, end)
})

const pages = computed(() => {
  return Math.ceil(tableItems.value.length / pagination.value.itemsPerPage)
})

//Search and price filters
function searchItems(refresh) {
  if (search.value) {
    let lowerCaseValue = search.value.split(' ').map((i) => i.trim().toLowerCase())
    tableItems.value = items.value.filter((item) =>
      lowerCaseValue.some(
        (word) =>
          item.item.toLowerCase().includes(word) || item.description.toLowerCase().includes(word)
      )
    )
  }
  if (refresh) {
    refreshPagination()
  }
}

function emptySearch() {
  search.value = ''
  tableItems.value = items.value
  priceFrom.value = null
  priceTo.value = null
  refreshPagination()
}

async function filterControl(event) {
  /// Decides to do combined filte with search or just filters///
  if (!event && search.value) {
    await searchItems(false)
    tableItems.value = await applyFilter(tableItems.value)
  } else if (!event && !search.value) {

    tableItems.value = await applyFilter(items.value)
  }
  if (!priceTo && !priceFrom) {
    isFiltered.value = false
  } else {
    isFiltered.value = true
  }

  refreshPagination()
}

function applyFilter(data) {
  ///Filters data based on price///
  if (priceFrom.value && !priceTo.value) {
    return data.filter((i) => i.price > priceFrom.value)
  } else if (priceTo.value) {
    return data.filter((i) => i.price > priceFrom.value && i.price < priceTo.value)
  } else {
    return data
  }
}

watch(showFavorites, async (newShowFavorites, oldShowFavorites) => {
  ///Retrieves Items marked as Favorites from LocalStorage///
  if (newShowFavorites) {
    tableItems.value = items.value.filter((i) => getFavorites.value.includes(i.barcode))
  } else if (!newShowFavorites && oldShowFavorites) {
    tableItems.value = items.value
  }
  refreshPagination()
})

//Requesting data from API and LocalStorage
async function checkLocalStorage() {
  
  if(productsStore.products.length <= 0){
    productsStore.products = await getItems()
  }

  return 
}

onMounted(async () => {
  await checkLocalStorage()
  initPage()
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
        <v-btn
          icon="mdi-magnify"
          color="orange"
          @click="searchItems(true)"
          class="align-self-start mt-n1"
        ></v-btn>
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
          @update:focused="filterControl($event)"
        ></v-text-field>

        <v-checkbox
          class="ma-2 w-10"
          density="compact"
          label="Favorites"
          v-model="showFavorites"
        ></v-checkbox>
      </v-col>
    </v-row>
  </div>
  <template v-if="pageItems">
    <div v-if="pageItems.length > 0">
      <div>total of {{ tableItems.length }} results</div>
      <div class="d-flex flex-wrap justify-start">
        <ItemCard v-for="(item, idx) in pageItems" :key="idx" v-bind:item="item"></ItemCard>
      </div>
      <div class="d-flex justify-center">
        <v-pagination
          :length="pages"
          v-model="currentPage"
          total-visible="5"
          :start="1"
        ></v-pagination>
      </div>
    </div>

    <div v-else-if="pageItems.length == 0">
      <div>There's no products matching your search</div>
    </div>
  </template>
  <template v-else>
    <div>There's nothing here</div>
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
