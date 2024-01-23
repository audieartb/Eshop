<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useAdminStore } from '../../stores/admin'
import { updateProduct, deleteProduct, createProduct } from '../../services/items'
import { useRouter } from 'vue-router'
import { useVuelidate } from '@vuelidate/core'
import {  required, numeric } from '@vuelidate/validators'

const props = defineProps(['mode'])
const adminStore = useAdminStore()
const router = useRouter()
const storeItem = reactive({...adminStore.productDetails })
const item = reactive({...storeItem })

const readonly = ref(true)

const rules = {
  title: { required},
  description: { required},
  price: { required, numeric},
  in_stock: { required, numeric},
  barcode: { required, numeric},
  sold: {numeric}
}

const v$ = useVuelidate(rules, item)
const changes = computed(() => {
  return Object.keys(item).some((field) => item[field] != storeItem[field])
})

const dateString = (date) => {
  var update = new Date(date)
  return `${update.toDateString()} at ${update.toLocaleTimeString()}`
}



async function save() {
  const result = await v$.value.$validate()
  if(!result) return

  if (props.mode == 'new') {
    item.image = ''
    const res = await createProduct(item)
    if (res.status == 201) {
      adminStore.productDetails = res.data
      readonly.value = true
      Object.assign(storeItem, adminStore.productDetails)
      Object.assign(item, storeItem)
    }
    return
  }

  const res = await updateProduct(item)
  if (res.status == 200) {

    adminStore.productDetails = res.data
    readonly.value = true
    Object.assign(storeItem, adminStore.productDetails)
    Object.assign(item, storeItem)
  }
}

const edit = () => {
  readonly.value = !readonly.value
  if (readonly.value) {
    Object.assign(item, storeItem)
  }
}

async function deleteProductBarcode(barcode) {
  if (!barcode) {
    alert('There is not an item to delete')
    return
  }
  let text = 'The selected Item will be deleted'
  if (!confirm(text)) {
    return
  }
  const res = await deleteProduct(barcode)
  if (res.status == 204) {
    alert('product has been removed')
    adminStore.productDetails = null
    router.push('/admin/products')
  }
}

onMounted(() => {
  if (props.mode == 'new') {
    readonly.value = false
  }
})
</script>
<template>
  <div>
    <v-card class="w-50">
      <div class="d-flex justify-space-between">
        <div>
          <v-card-title>{{ item.title }}</v-card-title>
          <v-card-subtitle v-if="item.updated_at">
            last updated: {{ dateString(item.updated_at) }}</v-card-subtitle
          >
          <v-card-text>{{ item.description }}</v-card-text>
        </div>
        <div class="pa-5">
          <v-btn
            class="ma-1"
            @click="edit"
            :icon="!readonly ? 'mdi-close' : 'mdi-file-edit'"
            :color="!readonly ? 'red' : 'blue'"
          ></v-btn>
          <v-btn
            class="ma-1"
            @click="save"
            :disabled="!changes"
            icon="mdi-content-save"
            color="green"
          ></v-btn>
          <v-btn
            class="ma-1"
            @click="deleteProductBarcode(item.barcode)"
            icon="mdi-trash-can"
            color="red"
          ></v-btn>
        </div>
      </div>
      <v-card-item>
        <v-row>
          <v-col>Barcode</v-col>
          <v-col
            ><v-text-field
              variant="outlined"
              :readonly="props.mode == 'new' ? false : true"
              v-model="item.barcode"
              required
              :error-messages="v$.barcode.$errors.map((e) => e.$message)"
              :append-icon="!readonly ? 'mdi-file-edit' : ''"
            ></v-text-field
          ></v-col>
        </v-row>
        <v-row>
          <v-col>Title</v-col>
          <v-col
            ><v-text-field
              variant="outlined"
              :readonly="readonly"
              v-model="item.title"
              :append-icon="!readonly ? 'mdi-file-edit' : ''" 
              required
              :error-messages="v$.title.$errors.map((e) => e.$message)"
            ></v-text-field
          ></v-col>
        </v-row>
        <v-row>
          <v-col>Description</v-col>
          <v-col
            ><v-textarea
              variant="outlined"
              :readonly="readonly"
              v-model="item.description"
              :append-icon="!readonly ? 'mdi-file-edit' : ''"
              required
              :error-messages="v$.description.$errors.map((e) => e.$message)"
            ></v-textarea
          ></v-col>
        </v-row>
        <v-row>
          <v-col>Price</v-col>
          <v-col
            ><v-text-field
              variant="outlined"
              :readonly="readonly"
              v-model="item.price"
              :append-icon="!readonly ? 'mdi-file-edit' : ''"
              required
              :error-messages="v$.price.$errors.map((e) => e.$message)"
            ></v-text-field
          ></v-col>
        </v-row>
        <v-row>
          <v-col>Sold</v-col>
          <v-col
            ><v-text-field
              variant="outlined"
              :readonly="readonly"
              v-model="item.sold"
              :append-icon="!readonly ? 'mdi-file-edit' : ''"
            ></v-text-field
          ></v-col>
        </v-row>
        <v-row>
          <v-col>In Stock</v-col>
          <v-col
            ><v-text-field
              variant="outlined"
              :readonly="readonly"
              v-model="item.in_stock"
              type="number"
              :append-icon="!readonly ? 'mdi-file-edit' : ''"
              required
              :error-messages="v$.in_stock.$errors.map((e) => e.$message)"
            ></v-text-field
          ></v-col>
        </v-row>
      </v-card-item>
    </v-card>
  </div>
</template>
