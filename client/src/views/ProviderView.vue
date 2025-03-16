<template>
  <h2 class="mb-2">Edit Provider: {{ data.name }} ({{ data.id }})</h2>

  <v-card>
    <v-card-text>
      <v-text-field label="Name" v-model="data.name"></v-text-field>

      <v-select
          label="Type"
          v-model="data.type"
          :items="['Hetzner']"
      ></v-select>

      <v-text-field label="API key" v-model="data.apiKey"></v-text-field>
      <v-text-field label="API Secret" v-model="data.apiSecret"></v-text-field>

      <v-btn color="primary" @click="update_provider">Save</v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import {onMounted, ref} from "vue";
import api from "@/api.js";
import {useRoute, useRouter} from "vue-router";

const route = useRoute()
const router = useRouter()

const data = ref({})

async function fetchData() {
  const response = await api.get('/providers/' + route.params.id);
  data.value = response.data
}

onMounted(async () => {
  fetchData();
});

function update_provider() {
  api.post('/providers/' + route.params.id, data.value)
      .then((_) => {
        router.push('/providers')
      })
      .catch((error) => {
        console.error('Error submitting form:', error)
      });
}

</script>