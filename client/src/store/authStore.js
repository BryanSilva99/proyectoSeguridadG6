import { create } from 'zustand';
import { login as loginApi, logout as logoutApi, refresh as refreshApi, me as meApi } from '../api/auth.api';
import { setAccessToken, setRefreshToken } from '../api/api.service';

// Read initial from localStorage
const storageUser = (() => {
  try {
    const u = localStorage.getItem('user');
    return u ? JSON.parse(u) : null;
  } catch (e) { return null; }
})();

const storageAccess = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
const storageRefresh = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null;

export const useAuthStore = create(set => ({
  user: storageUser,
  access: storageAccess,
  refresh: storageRefresh,
  loading: false,

  setUser: (user) => {
    set(() => ({ user }));
    if (user) localStorage.setItem('user', JSON.stringify(user));
    else localStorage.removeItem('user');
  },

  setTokens: ({ access, refresh }) => {
    set(() => ({ access, refresh }));
    if (access) setAccessToken(access); else setAccessToken(null);
    if (refresh) setRefreshToken(refresh); else setRefreshToken(null);
  },

  login: async (username, password) => {
    set(() => ({ loading: true }));
    try {
      const data = await loginApi({ username, password });
      // expected: data.access, data.refresh, data.user
      set(() => ({ loading: false }));
      set(() => ({ user: data.user }));
      if (data.user) localStorage.setItem('user', JSON.stringify(data.user));
      setAccessToken(data.access);
      setRefreshToken(data.refresh);
      set(() => ({ access: data.access, refresh: data.refresh }));
      return data;
    } catch (err) {
      set(() => ({ loading: false }));
      throw err;
    }
  },

  logout: async () => {
    set(() => ({ loading: true }));
    try {
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) await logoutApi(refresh);
    } catch (err) {
      // ignore errors during logout call
    } finally {
      // clear local state and storage
      set(() => ({ user: null, access: null, refresh: null, loading: false }));
      localStorage.clear();
      setAccessToken(null);
      setRefreshToken(null);
      window.location.href = '/login';
    }
  },

  refreshAccess: async () => {
    try {
      const refresh = localStorage.getItem('refresh_token');
      if (!refresh) throw new Error('No refresh token');
      const data = await refreshApi(refresh);
      // update tokens
      setAccessToken(data.access);
      setRefreshToken(data.refresh || refresh);
      set(() => ({ access: data.access, refresh: data.refresh || refresh }));
      return data;
    } catch (err) {
      // failed refresh -> force logout
      localStorage.clear();
      window.location.href = '/login';
      throw err;
    }
  },

  loadMe: async () => {
    set(() => ({ loading: true }));
    try {
      const data = await meApi();
      set(() => ({ user: data }));
      localStorage.setItem('user', JSON.stringify(data));
    } catch (err) {
      // ignore
    } finally {
      set(() => ({ loading: false }));
    }
  }
}));

export default useAuthStore;
