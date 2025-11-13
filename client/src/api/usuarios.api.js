import { apiClient } from './api.service';

export const getAllUsuarios = () => apiClient.get('/usuarios/');
export const getUsuario = (id) => apiClient.get(`/usuarios/${id}/`);
export const createUsuario = (usuario) => apiClient.post('/usuarios/', usuario);
export const deleteUsuario = (id) => apiClient.delete(`/usuarios/${id}/`);
export const updateUsuario = (id, usuario) => apiClient.put(`/usuarios/${id}/`, usuario);