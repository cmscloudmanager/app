import axios from 'axios';
import router from '@/router';  // Adjust the path to your router instance
import { useAuthStore } from '@/stores/userStore'; // If you use Pinia or Vuex for authentication

// Create Axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // Set your API base URL here
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add the authorization token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.token();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401 errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // If 401 Unauthorized, redirect to login page
      const authStore = useAuthStore();
      authStore.logout(); // Optionally log the user out from your state management
      router.push('/login'); // Adjust the route to your login page
    }
    return Promise.reject(error);
  }
);

export default api;