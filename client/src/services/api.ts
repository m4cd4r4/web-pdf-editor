import axios from 'axios';

// Create an axios instance with defaults
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to attach the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // If 401 Unauthorized, clear local storage and redirect to login
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication
const auth = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
};

// Documents
const documents = {
  getAll: () => api.get('/documents'),
  get: (id) => api.get(`/documents/${id}`),
  create: (formData) => api.post('/documents', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  update: (id, data) => api.put(`/documents/${id}`, data),
  delete: (id) => api.delete(`/documents/${id}`),
};

// PDF Operations
const pdf = {
  upload: (formData) => api.post('/pdf/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getDocument: (id) => api.get(`/pdf/${id}`),
  getContent: (id, version) => api.get(`/pdf/${id}/content${version ? `?version=${version}` : ''}`),
  extractText: (id, page) => api.get(`/pdf/${id}/extract-text${page !== undefined ? `?page=${page}` : ''}`),
  addText: (id, data) => api.post(`/pdf/${id}/add-text`, data),
  addImage: (id, data) => api.post(`/pdf/${id}/add-image`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  merge: (documentIds) => api.post('/pdf/merge', { document_ids: documentIds }),
};

// AI Operations
const ai = {
  processDocument: (id, query) => api.post(`/ai/process-document/${id}`, { query }),
  extractInformation: (id, infoType) => api.post(`/ai/extract-information/${id}`, { info_type: infoType }),
  summarize: (id, maxLength) => api.get(`/ai/summarize/${id}${maxLength ? `?max_length=${maxLength}` : ''}`),
};

// Form Operations
const forms = {
  getFormFields: (id) => api.get(`/pdf/${id}/form-fields`),
  fillForm: (id, data) => api.post(`/pdf/${id}/fill-form`, data),
  addFormField: (id, data) => api.post(`/pdf/${id}/add-form-field`, data),
};

// Conversion Operations
const conversion = {
  toDocument: (id, format) => api.post(`/pdf/${id}/convert`, { format }),
  toImage: (id, format, page, quality) => api.post(`/pdf/${id}/convert`, { 
    format, page, quality 
  }),
};

// Cloud Storage Operations
const cloudStorage = {
  listFiles: (provider, folderId, authToken) => api.get('/storage/list-files', {
    params: { provider, folder_id: folderId },
    headers: { 'Cloud-Auth-Token': authToken }
  }),
  download: (provider, fileId, authToken) => api.post('/storage/download', {
    provider, file_id: fileId
  }, {
    headers: { 'Cloud-Auth-Token': authToken }
  }),
  upload: (documentId, provider, folderId, authToken) => api.post(`/storage/upload/${documentId}`, {
    provider, folder_id: folderId
  }, {
    headers: { 'Cloud-Auth-Token': authToken }
  }),
};

export default {
  auth,
  documents,
  pdf,
  ai,
  forms,
  conversion,
  cloudStorage,
};
