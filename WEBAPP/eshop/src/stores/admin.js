import { defineStore } from 'pinia'

export const useAdminStore = defineStore('admin', {
  state: () => {
    return {
      email: '',
      auth_token: '',
      is_authenticated: false,
      orderDetails: {}
    }
  }
})
