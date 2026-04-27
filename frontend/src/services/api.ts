import axios, { AxiosInstance } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle responses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;

// Auth API
export const authAPI = {
  register: (data: any) => apiClient.post('/auth/register', data),
  login: (data: any) => apiClient.post('/auth/login', data),
  refresh: (data: any) => apiClient.post('/auth/refresh', data),
  me: () => apiClient.get('/auth/me'),
};

// Properties API
export const propertiesAPI = {
  getAll: (skip = 0, limit = 20) =>
    apiClient.get('/properties/', { params: { skip, limit } }),
  getById: (id: number) => apiClient.get(`/properties/${id}`),
  create: (data: any) => apiClient.post('/properties/', data),
  update: (id: number, data: any) => apiClient.put(`/properties/${id}`, data),
  delete: (id: number) => apiClient.delete(`/properties/${id}`),
  uploadImage: (id: number, file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post(`/properties/${id}/upload-image`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// Search API
export const searchAPI = {
  search: (filters: any) => apiClient.post('/search/properties', filters),
  getRegions: () => apiClient.get('/search/regions'),
  getDistricts: (region: string) =>
    apiClient.get(`/search/districts/${region}`),
};

// Listings API
export const listingsAPI = {
  getAll: (skip = 0, limit = 20) =>
    apiClient.get('/listings/', { params: { skip, limit } }),
  getPremium: (limit = 10) =>
    apiClient.get('/listings/premium', { params: { limit } }),
  getTop: (limit = 10) => apiClient.get('/listings/top', { params: { limit } }),
  create: (data: any) => apiClient.post('/listings/', data),
  makePremium: (id: number) => apiClient.post(`/listings/${id}/make-premium`),
  makeTop: (id: number) => apiClient.post(`/listings/${id}/make-top`),
};

// Users API
export const usersAPI = {
  getMe: () => apiClient.get('/users/me'),
  updateProfile: (data: any) => apiClient.put('/users/me', data),
  getById: (id: number) => apiClient.get(`/users/${id}`),
};

// Agents API
export const agentsAPI = {
  getAll: (skip = 0, limit = 20) =>
    apiClient.get('/agents/', { params: { skip, limit } }),
  getById: (id: number) => apiClient.get(`/agents/${id}`),
  getProperties: (id: number, skip = 0, limit = 20) =>
    apiClient.get(`/agents/${id}/properties`, { params: { skip, limit } }),
  createProfile: (data: any) => apiClient.post('/agents/profile', data),
};
