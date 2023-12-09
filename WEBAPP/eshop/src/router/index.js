import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CartView from '../views/CartView.vue'
import PaymentView from '../views/PaymentView.vue'
import OrderCompletedView from '../views/OrderCompletedView.vue'
import OrderHistoryView from '../views/OrderHistoryView.vue'
import OrderConfirmation from '../views/OrderConfirmation.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path:'/cart',
      name: 'cart',
      component: () => import('../views/CartView.vue'),
    },
    {
      path:'/payment',
      name: 'payment',
      component: PaymentView
    },
    {
      path: '/complete',
      name: 'complete',
      component: OrderCompletedView
    },
    {
      path: '/order/history',
      name: 'order_history',
      component: OrderHistoryView
    },
    {
      path: '/verification/:token',
      name: 'verification',
      component: OrderConfirmation,
      props: true
    }
  ]
})

export default router
