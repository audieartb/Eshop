import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useOrderStore = defineStore('order',  {

  state:()=>{
    return{
      orders:{}
    }
  }
})
