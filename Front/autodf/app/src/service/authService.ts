import api from "./axios";

export const TOKEN_KEY = "autodf_token";
export const REFRESH_TOKEN_KEY = "autodf_refresh_token";

const authService = {
  login: async (credentials: any) => {
    const response = await api.post("/api/auth/login/", credentials);
    if (response.data.access) {
      localStorage.setItem(TOKEN_KEY, response.data.access);
      localStorage.setItem(REFRESH_TOKEN_KEY, response.data.refresh);
    }
    return response.data;
  },

  register: async (userData: any) => {
    const response = await api.post("/api/auth/register/", userData);
    if (response.data.tokens) {
      localStorage.setItem(TOKEN_KEY, response.data.tokens.access);
      localStorage.setItem(REFRESH_TOKEN_KEY, response.data.tokens.refresh);
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    window.location.href = "/login";
  },

  getCurrentUser: async () => {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) return null;
    
    try {
      const response = await api.get("/api/auth/me/", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      return response.data;
    } catch (error) {
      return null;
    }
  },

  isAuthenticated: () => {
    if (typeof window === "undefined") return false;
    return !!localStorage.getItem(TOKEN_KEY);
  }
};

export default authService;
