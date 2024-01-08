<script setup>
import { useAdminStore } from '../../stores/admin';
const adminStore = useAdminStore()

const item = adminStore.productDetails

</script>
<template>
    <v-card>
        {{ item }}
    </v-card>
</template>