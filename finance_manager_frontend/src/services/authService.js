import api from './api';

// Endpoint for login (ensure the URL matches your backend route)
export const login = async (email, password) => {
  try {
    const response = await api.post('/login/', { email, password });
    return response.data;
  } catch (error) {
    console.error('Login error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

export const signup = async (userData) => {
  try {
    const response = await api.post('/register/', userData);
    return response.data;
  } catch (error) {
    console.error('Signup error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.detail || 'Signup failed');
  }
};
