<template>
  <h2 class="mb-2">New Project</h2>

  <v-stepper v-model="step"
             @update:model-value="() => validate() || step--"
             :items="['Information', 'Application', 'Finish']">
    <template v-slot:item.1>
      <v-card title="Information" flat>
        <v-text-field label="Name" v-model="data.name"></v-text-field>
        <v-text-field label="URL" v-model="data.url"></v-text-field>

        <v-select
            label="Type"
            v-model="data.type"
            :items="['WordPress']"
        ></v-select>
        <v-select
            label="Provider"
            v-model="data.provider"
            :items="['Hetzner']"
        ></v-select>
      </v-card>
    </template>

    <template v-slot:item.2>
      <v-card title="Application configuration" flat>
        <v-select
            v-model="data.region"
            label="Region"
            :items="regions"
        ></v-select>

        <v-select
            v-model="data.instance"
            label="Instance"
            outlined
            :items="instances"
        >
          <template v-slot:item="{ props, item }">
            <!-- Render category headers as non-selectable -->
            <v-list-item v-if="item.raw.group" class="font-weight-bold text-grey" disabled>
              {{ item.title }}
            </v-list-item>

            <!-- Render actual selectable items -->
            <v-list-item v-else v-bind="props"></v-list-item>
          </template>
        </v-select>
      </v-card>
    </template>

    <template v-slot:item.3>
      <v-card title="Finish" flat>
        Creating...

        <v-progress-linear indeterminate></v-progress-linear>
      </v-card>
    </template>
  </v-stepper>

  <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="3000">
    {{ snackbar.message }}
  </v-snackbar>
</template>

<script setup lang="ts">
import {ref, watch} from "vue";
import api from "@/api.js";

const step = ref(0)
const data = ref({})
const instances = ref([])
const regions = ref([])

const snackbar = ref({
  show: false,
  message: '',
  color: ''
})

const showSnackbar = (message, color) => {
  snackbar.value = {show: true, message, color};
}

function validate() {
  if (step.value == 2) {
    return data.value.name && data.value.url && data.value.type && data.value.provider
  }
  if (step.value == 3) {
    return data.value.instance && data.value.region
  }
}

watch(step, async (newStep) => {
  if (newStep === 2) {
    api.post('/instances', data.value)
        .then((response) => {
          instances.value = []
          regions.value = response.data['regions']

          console.log(response.data)
          response.data['plans'].forEach((item, index) => {
            instances.value.push({title: item['name'], group: true})

            item['options'].forEach((item, index) => {
              instances.value.push({title: item['name'], value: item['name']})
            })
          })
        })
        .catch((error) => {
          console.error('Error submitting form:', error)
        });
  } else if (newStep === 3) {
    api.post('/create-project', data.value)
        .then((_) => {
          showSnackbar('✅Project successfully created', 'success')
        })
        .catch((_) => {
          showSnackbar('Failed creating the project', 'error');
        });
  }
});
</script>