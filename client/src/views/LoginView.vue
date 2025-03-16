<template>
  <v-container class="d-flex justify-center align-center" style="min-height: 100vh;">
    <v-card class="elevation-12" max-width="400px" width="100%">
      <v-card-title class="headline">Login</v-card-title>

      <v-card-subtitle>
        Please enter your credentials
      </v-card-subtitle>

      <v-form v-model="valid" @submit.prevent="login">
        <v-text-field
            v-model="email"
            label="Email"
            :rules="[emailRule]"
            outlined
            dense
            required
        ></v-text-field>

        <v-text-field
            v-model="password"
            label="Password"
            :rules="[passwordRule]"
            type="password"
            outlined
            dense
            required
        ></v-text-field>

        <v-btn
            :disabled="!valid"
            color="primary"
            block
            @click="login">
          Login
        </v-btn>

        <v-alert v-if="loginError" type="error" dismissible>
          Invalid email or password.
        </v-alert>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      emailRule: [
        v => !!v || 'Email is required',
        v => /.+@.+\..+/.test(v) || 'Email must be valid'
      ],
      passwordRule: [
        v => !!v || 'Password is required',
        v => v.length >= 6 || 'Password must be at least 6 characters'
      ]
    };
  },
};
</script>

<script setup>
import {ref} from "vue";
import {useRouter} from "vue-router";
import {useAuthStore} from "@/stores/userStore.js";
import api from "@/api.js";

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const valid = ref(false)
const loginError = ref(false)

async function login() {
  api.post('/login', {email: email.value, password: password.value})
      .then((response) => {
        if (response.data.access_token) {
          authStore.login(response.data.access_token)
          router.push('/projects')
        } else {
          loginError.value = true
        }
      })
      .catch((error) => {
        console.error('Login error:', error)
        loginError.value = true
      });
}
</script>

<style scoped>
.v-card {
  padding: 16px;
}
</style>