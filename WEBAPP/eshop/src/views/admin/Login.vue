<script setup>
import { ref } from 'vue'
import { login } from '../../services/adminLogin'
import { useAdminStore } from '../../stores/admin'
import { useRouter } from 'vue-router';
const adminStore = useAdminStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const show = ref(false)
var form_data = new FormData()

async function sendLogin() {
  form_data.append('username', username.value)
  form_data.append('password', password.value)
  login(form_data)
    .then((data) => {
      adminStore.auth_token = data.access_token
      adminStore.email = username.value
      adminStore.is_authenticated = true
      router.push('dashboard')
    })
    .catch((err) => {
      console.log(err)
    })
}
</script>

<template>
  <div class="form-parent">
    <div class="form">
      <div>Login as Admin</div>
      <v-form>
        <v-text-field
          v-model="username"
          type="text"
          name="username-input"
          label="username"
          variant="outlined"
        ></v-text-field>
        <v-text-field
          v-model="password"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show ? 'text' : 'password'"
          name="password-input"
          variant="outlined"
          label="password"
          @click:append="show = !show"
        ></v-text-field>
        <v-btn @click="sendLogin">Log in</v-btn>
      </v-form>
    </div>
  </div>
</template>

<style scoped>
.form-parent {
  display: flex;
  justify-content: center;
  align-items: center;
}

.form {
  width: 350px;
  height: 200px;
  padding: 0px;
}
</style>
