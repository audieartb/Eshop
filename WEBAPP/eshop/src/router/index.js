import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CartView from '../views/CartView.vue'
import PaymentView from '../views/PaymentView.vue'
import OrderCompletedView from '../views/OrderCompletedView.vue'
import OrderRequestView from '../views/OrderRequestView.vue'
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
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
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
      path: '/order/request',
      name: 'order_request',
      component: OrderRequestView
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
