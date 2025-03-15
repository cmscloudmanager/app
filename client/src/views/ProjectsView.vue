<template>
  <v-row justify="space-between" class="mb-2">
    <v-col cols="auto">
      <h2>Projects</h2>
    </v-col>

    <!-- Add Button -->
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
    @update:options="loadItems"
  ></v-data-table-server>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const itemsPerPage = ref(10)
const headers = ref([
  { title: 'Name', key: 'name'},
  { title: 'Type', key: 'type'},
  { title: 'URL', key: 'url'},
  { title: 'Version', key: 'version'},
  { title: 'Extra', key: 'extra'},
])
const search = ref('')
const items = ref([])
const loading = ref(true)
const totalItems = ref(0)

// Function to fetch data from an API
const fetchData = async () => {
  loading.value = true
  try {
    const response = await fetch(import.meta.env.VITE_API_URL + '/projects')
    const data = await response.json()
    items.value = data.items
    totalItems.value = data.total
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    loading.value = false
  }
}

// Fetch data when component mounts
onMounted(() => {
  fetchData()
})

function onAddClick() {

}
</script>