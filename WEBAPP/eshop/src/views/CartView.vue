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
  <div class="d-flex">
    <template v-if="carts[currentCart]">
      <div class="d-flex align-center flex-column">
        <v-card
          v-for="(item, idx) in carts[currentCart].items"
          width="400"
          :title="item.barcode"
          subtitle="This is a subtitle"
          text="This is content"
          class="m-3"
        ></v-card>
      </div>
    </template>
    <div>
    <FormPersonal></FormPersonal>
     
    </div>
  </div>
</template>
