<template>
  <h2 class="mb-2">Edit Project: {{ data.name }} ({{ data.id }})</h2>

  <v-card>
    <v-tabs
        v-model="tab"
        bg-color="primary"
    >
      <v-tab value="information">Information</v-tab>
      <v-tab value="config">Config</v-tab>
    </v-tabs>

    <v-card-text>
      <v-tabs-window v-model="tab">
        <v-tabs-window-item value="information">
          <v-card-text>
            <v-text-field label="Name" v-model="data.name"></v-text-field>

            <v-btn color="primary" @click="update_provider">Save</v-btn>
          </v-card-text>
        </v-tabs-window-item>

        <v-tabs-window-item value="config">
          <v-code v-html="formattedYamlContent"  style="white-space: pre-wrap;" />
        </v-tabs-window-item>
      </v-tabs-window>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
import api from "@/api.js";
import {useRoute, useRouter} from "vue-router";

const route = useRoute()
const router = useRouter()

const tab = ref(null)
const data = ref({})

async function fetchData() {
  const response = await api.get('/projects/' + route.params.id);
  data.value = response.data
}

onMounted(async () => {
  fetchData();
});

function update_provider() {
  api.post('/projects/' + route.params.id, data.value)
      .then((_) => {
        router.push('/projects')
      })
      .catch((error) => {
        console.error('Error submitting form:', error)
      });
}

const formattedYamlContent = computed(() => {
  return data.value.manifest.replace(/\n/g, '<br/>');
});

</script>