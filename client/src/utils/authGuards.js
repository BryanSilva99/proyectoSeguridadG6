import { redirect } from 'react-router-dom';

/**
 * Verifica que el usuario esté autenticado
 * @returns {Object|null} Usuario actual o redirect a login
 */
export const requireAuth = () => {
  try {
    const userStr = localStorage.getItem('user');
    if (!userStr) return redirect('/login');
    return JSON.parse(userStr);
  } catch (err) {
    return redirect('/login');
  }
};

/**
 * Verifica que el usuario sea administrador
 * @returns {Object|null} Usuario administrador o redirect a unauthorized/login
 */
export const requireAdmin = () => {
  try {
    const userStr = localStorage.getItem('user');
    if (!userStr) return redirect('/login');
    const user = JSON.parse(userStr);
    if (user.type !== 'administrador') {
      return redirect('/unauthorized');
    }
    return user;
  } catch (err) {
    return redirect('/login');
  }
};

/**
 * Verifica que el usuario sea cliente
 * @returns {Object|null} Usuario cliente o redirect a unauthorized/login
 */
export const requireCliente = () => {
  try {
    const userStr = localStorage.getItem('user');
    if (!userStr) return redirect('/login');
    const user = JSON.parse(userStr);
    if (user.type !== 'cliente') {
      return redirect('/unauthorized');
    }
    return user;
  } catch (err) {
    return redirect('/login');
  }
};
