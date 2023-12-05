<script setup>
import { RouterLink, RouterView } from 'vue-router'
import MainBar from './components/MainBar.vue';
import { onMounted } from 'vue';
import { useProductStore } from '@/stores/products'
import { getItems } from './services/items';

const productsStore = useProductStore()
onMounted(async()=>{
  productsStore.products = await getItems()
})
</script>

<template>
  <v-app>
    <header>
      <link
        href="https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css"
        rel="stylesheet"
      />
    </header>
   <MainBar></MainBar>
    <div class="main">
      <RouterView />
    </div>
  </v-app>
</template>

<style scoped>

</style>
