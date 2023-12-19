<script setup>
import { ref } from 'vue'
import { RouterLink , useRouter} from 'vue-router';

const router = useRouter()
const views = ref([
{
        name: 'Orders',
        id: 6,
        icon: 'mdi-receipt',
        link: '/admin/orders'
    },
    {
        name: 'Products',
        id: 7,
        icon: 'mdi-drawing-box',
        link: '/admin/products'
    },
    {
        name: 'Dashboard',
        id: 2,
        icon: 'mdi-history',
        link: '/admin/dashboard'
    },
    {
        name: 'Import Products',
        id: 4,
        icon: 'mdi-database-import',
        link: '/admin/import'
    },
])

function routerTo(url){
    router.push(url)
}

</script>
<template>
  <div>
    <v-navigation-drawer expand-on-hover rail permanent>
      <v-list-item title="Store" prepend-icon="mdi-home-analytics" subtitle="Admin Panel"></v-list-item>
      <v-divider></v-divider>
      <v-list-item
        v-for="tab in views"
        link
        :title="tab.name"
        :prepend-icon="tab.icon"
        @click="routerTo(tab.link)"
      ></v-list-item>
   
    </v-navigation-drawer>
  </div>
</template>
