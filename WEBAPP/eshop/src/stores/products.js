import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useProductStore = defineStore('products',  {

  state:()=>{
    return{
      products:[
        {
          barcode: '100000000011',
          item: 'Coffee Maker',
          description: 'Programmable coffee maker with timer',
          in_stock: 15,
          price: 49.99,
          sold: 5
        },
        {
          barcode: '100000000012',
          item: 'Smart TV',
          description: '4K smart TV for your entertainment',
          in_stock: 14,
          price: 699.99,
          sold: 3
        },
        {
          barcode: '100000000013',
          item: 'Sofa',
          description: 'Comfortable sofa for your living room',
          in_stock: 25,
          price: 499.99,
          sold: 6
        },
        {
          barcode: '100000000014',
          item: 'Gaming Chair',
          description: 'Comfortable gaming chair for gamers',
          in_stock: 19,
          price: 159.99,
          sold: 6
        },
        {
          barcode: '100000000011',
          item: 'Coffee Maker',
          description: 'Programmable coffee maker with timer',
          in_stock: 15,
          price: 49.99,
          sold: 5
        },
        {
          barcode: '100000000012',
          item: 'Smart TV',
          description: '4K smart TV for your entertainment',
          in_stock: 14,
          price: 699.99,
          sold: 3
        },
        {
          barcode: '100000000013',
          item: 'Sofa',
          description: 'Comfortable sofa for your living room',
          in_stock: 25,
          price: 499.99,
          sold: 6
        },
        {
          barcode: '100000000014',
          item: 'Gaming Chair',
          description: 'Comfortable gaming chair for gamers',
          in_stock: 19,
          price: 159.99,
          sold: 6
        },
        {
          barcode: "100000000017",
          item: "Gardening Gloves",
          description: "Durable gloves for gardening",
          in_stock: 55,
          price: 9.99,
          sold: 18
        },
        {
          barcode: "100000000018",
          item: "Bicycle",
          description: 'Mountain bike for adventurous rides',
          in_stock: 12,
          price: 279.95,
          sold: 4
        },
        {
          barcode: '100000000019',
          item: "Blender",
          description: 'High-speed blender for smoothies',
          in_stock: 30,
          price: 59.99,
          sold: 7
        },
        {
          barcode: '100000000020',
          item: 'Dishwasher',
          description: 'Compact dishwasher for your kitchen',
          in_stock: 8,
          price: 399.95,
          sold: 3
        }
      ]
    }
  }
})
