<script setup>
defineProps({})
</script>

<template>
  <div>
    <v-navigation-drawer :elevation="2">
      Home
      <template v-slot:append>
        <v-btn icon="mdi-heart"></v-btn>

        <v-btn icon="mdi-magnify"></v-btn>

        <v-btn icon="mdi-dots-vertical"></v-btn>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<style scoped>
div {
  position: fixed;
  overflow: hidden;
}
</style>
