import api from './api';

// Endpoint for login (ensure the URL matches your backend route)
export const login = async (email, password) => {
  try {
    const response = await api.post('/login/', { email, password });  // Note the trailing slash
    return response.data;
  } catch (error) {
    // Log or handle error as needed
    console.error('Login error:', error.response?.data || error.message);
    throw error;
  }
};

// Endpoint for signup (ensure the URL matches your backend route)
export const signup = async (userData) => {
  try {
    const response = await api.post('/register/', userData);  // Note the trailing slash
    return response.data;
  } catch (error) {
    // Log or handle error as needed
    console.error('Signup error:', error.response?.data || error.message);
    throw error;
  }
};
