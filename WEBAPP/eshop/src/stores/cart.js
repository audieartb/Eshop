import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => {
    return {
      email: '',
      currentCart: null,
      carts: {},
      favorites: [],
      form_data: {},
      in_progress: false
    }
  },
  getters: {
    itemsInCart(state) {
      return !state.currentCart ? null : state.carts[state.currentCart]
    },
    justItems(state) {
      let items = !state.currentCart ? null : state.carts[state.currentCart].items
      return items
    },
    getFavorites(state) {
      return state.favorites
    },
    getCarts(state){
      return Object.keys(state.carts)
    }
  },
  actions: {
    createCart() {
      if (this.getCarts.length >= 3) {
        return false
      } else {
        let cart = {
          items: {},
          total: 0.00,
          total_items: 0
        }
        this.setCurrentCart(null)
        this.carts[this.currentCart] = cart
        this.carts[this.currentCart].id = this.currentCart
      }
      return true
    },
    setCurrentCart(cartId) {
      if(!cartId){
        this.currentCart = String(Date.now())
      }else{
        this.currentCart = cartId
      }
      
    },
    async addToCart(item) {
      if (!this.currentCart) {
        await this.createCart()
      }

      if (!this.inCart(item.barcode)) {
        let newItem = {
          barcode: item.barcode,
          qty: 1,
          price: item.price,
          img: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg',
          title: item.item
        }
        this.carts[this.currentCart].items[item.barcode] = newItem
      } else {
        this.carts[this.currentCart].items[item.barcode].qty++
      }
      this.carts[this.currentCart].total += item.price
      this.carts[this.currentCart].total_items++
    },
    removeOneFromCart(item) {
      let barcode = item.barcode
      if (!this.inCart(barcode)) {
        return
      } else if (this.carts[this.currentCart].items[barcode].qty == 1) {
        delete this.carts[this.currentCart].items[barcode]
      } else {
        this.carts[this.currentCart].items[barcode].qty--
      }
      this.carts[this.currentCart].total -= item.price
      this.carts[this.currentCart].total_items--
      if (this.carts[this.currentCart].total_items <= 0) {
        this.deleteCart(this.currentCart)
      }
    },
    inCart(barcode) {
      return !this.carts[this.currentCart].items[barcode] ? false : true
    },
    deleteCart(cartId) {
      delete this.carts[cartId]
      if(this.getCarts.length>0){
        this.currentCart = this.getCarts[0]
      }else{
        this.currentCart = null
      }
      return true
    }
  }
})
