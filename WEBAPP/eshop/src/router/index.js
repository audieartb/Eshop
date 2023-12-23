import { createRouter, createWebHistory } from 'vue-router'
import {useAdminStore } from '../stores/admin'
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
import ProductDetailsView from '../views/admin/ProductDetailsView.vue'
function isAdmin(to, from, next){
  const adminStore = useAdminStore()
  if(adminStore.is_authenticated && adminStore.auth_token){
    return next()
  }else{
    return next('admin/login')
  }
}

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
      beforeEnter:[isAdmin]
    },
    {
      path: '/admin/products',
      name: 'products',
      component: Products,
      beforeEnter:[isAdmin]
    },
    {
      path: '/admin/orders',
      name: 'admin-orders',
      component: Orders,
      beforeEnter:[isAdmin]
  
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
      beforeEnter:[isAdmin]
    },
    {
      path: '/admin/import',
      name: 'import',
      component: ImportView,
      beforeEnter:[isAdmin]
    },
    {
      path: '/admin/products/details',
      name: 'import',
      component: ProductDetailsView,
      beforeEnter:[isAdmin]
    },

  ]
})

export default router
