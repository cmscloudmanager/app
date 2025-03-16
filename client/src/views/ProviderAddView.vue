<template>
  <h2 class="mb-2">New Provider</h2>

  <v-card>
    <v-card-text>
      <v-text-field label="Name" v-model="data.name"></v-text-field>

      <v-select
          label="Type"
          v-model="data.type"
          :items="['Hetzner']"
      ></v-select>

      <v-text-field label="API key" v-model="data.api_key"></v-text-field>
      <v-text-field label="API Secret" v-model="data.api_secret"></v-text-field>

      <v-btn color="primary" @click="add_provider">Submit</v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import {ref} from "vue";
import api from "@/api.js";
import {useRouter} from "vue-router";

const router = useRouter()

const data = ref({})

function add_provider() {
  api.post('/add-provider', data.value)
      .then((_) => {
        router.push('/providers')
      })
      .catch((error) => {
        console.error('Error submitting form:', error)
      });
}

</script>