import React from 'react';
import { Link } from 'react-router-dom';

export const NotFoundPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div style={{ maxWidth: 720 }} className="text-center p-8 bg-white rounded-lg shadow-md">
        <h1 style={{ fontSize: 72, margin: 0 }} className="text-gray-800">404</h1>
        <h2 className="text-2xl mt-2">Página no encontrada</h2>
        <p className="text-gray-600 mt-4">La ruta que intentaste abrir no existe o fue movida.</p>
        <div className="mt-6">
          <Link to="/login" className="inline-block bg-black text-white px-6 py-2 rounded-lg">Ir al login</Link>
          <Link to="/app/libros" className="inline-block ml-4 text-black underline">Ir a la aplicación</Link>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage;
