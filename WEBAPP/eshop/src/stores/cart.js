import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => {
    return {
      email: '',
      currentCart: null,
      carts: {}
    }
  },
  getters: {
    itemsInCart(state) {
      return !state.currentCart ? null : state.carts[state.currentCart]
    }
  },
  actions: {
    createCart() {
      if (this.carts.length >= 3) {
        return
      } else {
        let cart = {
          items: {},
          total: 0
        }
        this.setCurrentCart()
        this.carts[this.currentCart] = cart
      }
    },
    setCurrentCart() {
      this.currentCart = String(Date.now())
    },
    async addToCart(item) {
      if (!this.currentCart) {
        this.createCart()
      }

      if (!this.inCart(item.barcode)) {
        let newItem = {
          barcode: item.barcode,
          qty: 1,
          price: item.price
        }
        this.carts[this.currentCart].items[item.barcode] = newItem
      } else {
        this.carts[this.currentCart].items[item.barcode].qty++
      }
      this.carts[this.currentCart].total += item.price

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
      console.log('finish remove')
    },
    inCart(barcode) {
      console.log('checking in cart')
      return !this.carts[this.currentCart].items[barcode] ? false : true
    }
  }
})
