<script setup>
import axios from 'axios';
const props = defineProps(['token'])


async function checkToken(){

    res = await axios.post() 
}
</script>
<template>
    <div>
        Order Confirmation{{ token }}
    </div>
</template>