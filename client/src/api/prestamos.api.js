import { apiClient } from './api.service';

export const getAllPrestamos = () => apiClient.get('/prestamos/');
export const getPrestamo = (id) => apiClient.get(`/prestamos/${id}/`);
export const createPrestamo = (prestamo) => apiClient.post('/prestamos/', prestamo);
export const deletePrestamo = (id) => apiClient.delete(`/prestamos/${id}/`);
export const updatePrestamo = (id, prestamo) => apiClient.put(`/prestamos/${id}/`, prestamo);