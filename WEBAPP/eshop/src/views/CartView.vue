<script setup>
import { ref, reactive } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'
import FormPersonal from '../components/FormPersonal.vue';

const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)
</script>

<template>
  <div class="d-flex justify-space-between">
    <template v-if="carts[currentCart]">
      <div class="d-flex align-start flex-column w-50">
        <v-card
          v-for="(item, idx) in carts[currentCart].items"
          width="400"
          :title="item.barcode"
          subtitle="This is a subtitle"
          text="This is content"
          class="mb-5"
        ></v-card>
      </div>
    </template>
    <div class="w-50">
    <FormPersonal></FormPersonal>
     
    </div>
  </div>
</template>
