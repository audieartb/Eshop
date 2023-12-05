<script setup>
import axios from 'axios';
import { onMounted , ref} from 'vue';
const props = defineProps(['token'])
const valid = ref(false)
const data = ref(null)
const confirmation_url = 'http://localhost:8000/api/orders/confirmation?token='
async function checkToken(){

    const res = await axios.post(confirmation_url+props.token) 
    if(res.status == 200){
        valid.value = true
        data.value = res.data
    }else{

    }
}

onMounted(()=>{
    checkToken()
})
</script>
<template>
    <div v-if="valid">
        Your Order has been confirmed, you will received more updates on {{ data.email }} 
    </div>
    <div v-else>
        This link is no longer valid
    </div>
</template>