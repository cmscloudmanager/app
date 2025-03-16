import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: localStorage.getItem('auth_token') ? true : false,
  }),
  actions: {
    login(access_token) {
      this.isAuthenticated = true;
      localStorage.setItem('auth_token', access_token);
    },
    logout() {
      this.isAuthenticated = false;
      localStorage.removeItem('auth_token');
    },
    token() {
      return localStorage.getItem('auth_token')
    },
  },
});