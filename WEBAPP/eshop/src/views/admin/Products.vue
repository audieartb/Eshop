<script setup>
import ProductsTable from '../../components/admin/ProductsTable.vue'
import Navigation from '../../components/admin/Navigation.vue'
import AdminTable from '../../components/admin/AdminTable.vue'
import { getCount, itemsPagination } from '../../services/items'

const tableColums = [
  {
    key: 'title',
    name: 'Title'
  },
  {
    key: 'barcode',
    name: 'Barcode'
  },
  {
    key: 'created_at',
    name: 'Created On'
  },
  {
    key: 'updated_at',
    name: 'Updated At'
  },
  {
    key: 'price',
    name: 'Price'
  },
  {
    key: 'in_stock',
    name: 'Stock'
  },
  {
    key: 'sold',
    name: 'Sold'
  }
]

async function setUp(){
  itemsPagination()
}
</script>

<template>
  <div class="admin-data-container">
    <div class="dashboard-title">Products</div>
    <AdminTable :columns="tableColums" @get-data=""></AdminTable>
  </div>
</template>
