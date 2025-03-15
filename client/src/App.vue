<template>
  <v-responsive class="border rounded">
    <v-app :theme="theme">
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
          <v-list-item prepend-icon="mdi-folder" title="Projects" to="projects"></v-list-item>
          <v-list-item prepend-icon="mdi-account-multiple" title="Users" to="users"></v-list-item>
          <v-list-item prepend-icon="mdi-cogs" title="Settings" to="settings"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main>
        <v-container>
          <RouterView />
        </v-container>
      </v-main>
    </v-app>
  </v-responsive>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'

const drawer = ref(true)
const theme = ref('dark')

function onClick () {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}
</script>