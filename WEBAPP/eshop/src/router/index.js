import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import PaymentView from '../views/PaymentView.vue'
import OrderCompletedView from '../views/OrderCompletedView.vue'
import OrderHistoryView from '../views/OrderHistoryView.vue'
import OrderConfirmation from '../views/OrderConfirmation.vue'
import DashboardView from '../views/admin/DashboardView.vue'
import Login from '../views/admin/Login.vue'
import Orders from '../views/admin/Orders.vue'
import Products from '../views/admin/Products.vue'

import OrderDetails from '../views/admin/OrderDetails.vue'
import ImportView from '../views/admin/ImportView.vue'

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
    },
    {
      path: '/admin/dashboard',
      name: 'monthly',
      component: DashboardView,
    },
    {
      path: '/admin/products',
      name: 'products',
      component: Products,
    },
    {
      path: '/admin/orders',
      name: 'admin-orders',
      component: Orders,
  
    },
    {
      path: '/admin/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/admin/order/details',
      name: 'order-details',
      component: OrderDetails,
    },
    {
      path: '/admin/import',
      name: 'import',
      component: ImportView,
    },

  ]
})

export default router
