<script setup>
import ProductDetailsCard from '../../components/admin/ProductDetailsCard.vue';
const props = defineProps(['mode'])
</script>
<template>
    <div class="dashboard-title">Product details</div>
    <ProductDetailsCard :mode="props.mode">
    </ProductDetailsCard>
</template>