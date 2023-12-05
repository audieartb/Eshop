import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useProductStore = defineStore('products',  {

  state:()=>{
    return{
      products:[]
    }
  }
})
