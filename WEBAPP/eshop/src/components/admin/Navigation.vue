<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAdminStore } from '../../stores/admin'
const adminStore = useAdminStore()
const router = useRouter()
const views = ref([
  {
    name: 'Dashboard',
    id: 1,
    icon: 'mdi-monitor-dashboard',
    link: '/admin/dashboard'
  },
  {
    name: 'Last 24Hrs.',
    id:2,
    icon: 'mdi-history',
    link: '/admin/orders/recent'
  },

  {
    name: 'Orders',
    id: 3,
    icon: 'mdi-receipt',
    link: '/admin/orders'
  },
  {
    name: 'Products',
    id: 4,
    icon: 'mdi-drawing-box',
    link: '/admin/products'
  },

  {
    name: 'Import Products',
    id: 5,
    icon: 'mdi-database-import',
    link: '/admin/import'
  }
])

function routerTo(url) {
  router.push(url)
}
</script>
<template>
  <div v-if="adminStore.is_authenticated">
    <v-navigation-drawer expand-on-hover rail permanent>
      <v-list-item
        title="Store"
        prepend-icon="mdi-home-analytics"
        subtitle="Admin Panel"
      ></v-list-item>
      <v-divider></v-divider>
      <v-list-item
        v-for="tab in views"
        link
        :title="tab.name"
        :prepend-icon="tab.icon"
        @click="routerTo(tab.link)"
      ></v-list-item>
    </v-navigation-drawer>
    {{ adminStore.is_authenticated }}
  </div>
</template>
