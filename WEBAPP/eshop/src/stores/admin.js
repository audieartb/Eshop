import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAdminStore = defineStore('admin',  {

  state:()=>{
    return{
      email:'',
      auth_token: '',
      is_authenticated: true,
      orderDetails: {}
    }
  }
})
