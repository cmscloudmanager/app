<template>
    <h1>Projects</h1>

    <v-data-table-server
    v-model:items-per-page="itemsPerPage"
    :headers="headers"
    :items="serverItems"
    :items-length="totalItems"
    :loading="loading"
    :search="search"
    item-value="name"
    @update:options="loadItems"
  ></v-data-table-server>
</template>

<script setup>
  import { ref } from 'vue'

  const desserts = [
    {
      name: 'My WordPress site',
      type: 'WordPress',
      url: 'javiercasares.com',
      version: '6.2',
      extra: 'PHP 5.6',
    },
  ]
  const FakeAPI = {
    async fetch ({ page, itemsPerPage, sortBy }) {
      return new Promise(resolve => {
        setTimeout(() => {
          const start = (page - 1) * itemsPerPage
          const end = start + itemsPerPage
          const items = desserts.slice()
          if (sortBy.length) {
            const sortKey = sortBy[0].key
            const sortOrder = sortBy[0].order
            items.sort((a, b) => {
              const aValue = a[sortKey]
              const bValue = b[sortKey]
              return sortOrder === 'desc' ? bValue - aValue : aValue - bValue
            })
          }
          const paginated = items.slice(start, end === -1 ? undefined : end)
          resolve({ items: paginated, total: items.length })
        }, 500)
      })
    },
  }
  const itemsPerPage = ref(5)
  const headers = ref([
    { title: 'Name', key: 'name'},
    { title: 'Type', key: 'type'},
    { title: 'URL', key: 'url'},
    { title: 'Version', key: 'version'},
    { title: 'Extra', key: 'extra'},
  ])
  const search = ref('')
  const serverItems = ref([])
  const loading = ref(true)
  const totalItems = ref(0)
  function loadItems ({ page, itemsPerPage, sortBy }) {
    loading.value = true
    FakeAPI.fetch({ page, itemsPerPage, sortBy }).then(({ items, total }) => {
      serverItems.value = items
      totalItems.value = total
      loading.value = false
    })
  }
</script>