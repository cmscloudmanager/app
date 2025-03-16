<template>
  <v-responsive>
    <v-app :theme="theme" v-if="isAuthenticated">
      <v-app-bar>
        <template v-slot:prepend>
          <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        </template>

        <v-app-bar-title>CMS Cloud Manager</v-app-bar-title>

        <v-spacer></v-spacer>

        <v-btn
          :prepend-icon="theme === 'light' ? 'mdi-weather-sunny' : 'mdi-weather-night'"
          text="Toggle Theme"
          slim
          @click="onClick"
        ></v-btn>
      </v-app-bar>

      <v-navigation-drawer v-model="drawer">
        <v-list>
          <v-list-item
            prepend-avatar="https://randomuser.me/api/portraits/men/85.jpg"
            title="Javier Casares"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-post" title="Projects" to="/projects"></v-list-item>
          <v-list-item prepend-icon="mdi-connection" title="Providers" to="/providers"></v-list-item>
          <v-list-item prepend-icon="mdi-account-multiple" title="Users" to="/users"></v-list-item>
          <v-list-item prepend-icon="mdi-cogs" title="Settings" to="/settings"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main>
        <v-container>
          <RouterView />
        </v-container>
      </v-main>
    </v-app>

    <v-app v-if="!isAuthenticated">
      <RouterView />
    </v-app>
  </v-responsive>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { ref } from 'vue'
import {useAuthStore} from "@/stores/userStore.js";
import {storeToRefs} from "pinia";

const drawer = ref(true)
const theme = ref('dark')
const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)

function onClick () {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}
</script>