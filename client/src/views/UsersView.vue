<template>
  <v-row justify="space-between" class="mb-2">
    <v-col cols="auto">
      <h2>Users</h2>
    </v-col>

    <v-col cols="auto">
      <v-btn color="primary" @click="onAddClick">
        <v-icon left>mdi-plus</v-icon>
        Add
      </v-btn>
    </v-col>
  </v-row>

  <v-data-table-server
      v-model:items-per-page="itemsPerPage"
      :headers="headers"
      :items="items"
      :items-length="totalItems"
      :loading="loading"
      :search="search"
      item-value="name"
      @update:options="fetchData"
  ></v-data-table-server>
</template>

<script setup>
import {ref} from 'vue'
import api from "@/api.js";

const itemsPerPage = ref(10)
const headers = ref([
  {title: 'ID', key: 'id'},
  {title: 'Name', key: 'name'},
  {title: 'E-Mail', key: 'email'},
])
const search = ref('')
const items = ref([])
const loading = ref(true)
const totalItems = ref(0)

const fetchData = async () => {
  loading.value = true;

  try {
    const response = await api.get('/users');
    const data = response.data
    items.value = data.items
    totalItems.value = data.total
  } catch (error) {
    console.error('Error fetching data:', error);
  } finally {
    loading.value = false;
  }
}

function onAddClick() {
  alert("Not Implemented")
}

</script>