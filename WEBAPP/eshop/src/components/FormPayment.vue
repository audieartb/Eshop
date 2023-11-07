<script setup>


</script>

<template>
    <div>
        <form action="">
        <v-text-field label="Name on Card" :error-messages="'error'" required></v-text-field>
        <v-text-field label="Card Number" :error-messages="'error'" required></v-text-field>
        <v-text-field label="Cvv" :error-messages="'error'" required></v-text-field>
        <v-text-field label="Expiration Date" :error-messages="'error'" required></v-text-field>
        <v-btn class="me-4">Complete Order</v-btn>
      </form>
    </div>
</template>