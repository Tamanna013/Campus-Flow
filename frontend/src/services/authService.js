import api from "./api";

export const authService = {
  register: (data) => api.post("/auth/register/", data),
  login: (email, password) => api.post("/auth/login/", { email, password }),
  logout: () => api.post("/auth/logout/"),
  verifyEmail: (token) => api.post("/auth/verify_email/", { token }),
  getCurrentUser: () => api.get("/users/me/"),
  updateProfile: (data) => api.put("/users/me/", data),
  changePassword: (data) => api.post("/users/me/change_password/", data),
};
