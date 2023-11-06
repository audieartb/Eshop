<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { storeToRefs } from 'pinia'

const store = useCartStore()
const { carts } = storeToRefs(store)
const { currentCart } = storeToRefs(store)

</script>

<template>
  <div class="d-flex align-center flex-column">
    <template v-if="carts[currentCart]">
        <v-card v-for="(item, idx) in carts[currentCart].items"
      width="400"
      :title="item.barcode"
      subtitle="This is a subtitle"
      text="This is content"
    ></v-card>
    </template>
  </div>
</template>
