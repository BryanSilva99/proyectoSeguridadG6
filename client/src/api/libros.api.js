// Se creará un script que enviará una petición al backend
import { apiClient } from './api.service';

// Obtener todos los libros
export const getAllLibros = () => apiClient.get('/libros/');

// Crear un nuevo libro
export const createLibro = (libro) => apiClient.post('/libros/', libro);

// Actualizar un libro existente
export const updateLibro = (isbn, libro) => apiClient.put(`/libros/${isbn}/`, libro);

// Obtener un libro específico
export const getLibro = (isbn) => apiClient.get(`/libros/${isbn}/`);

// Eliminar un libro
export const deleteLibro = (isbn) => apiClient.delete(`/libros/${isbn}/`);
