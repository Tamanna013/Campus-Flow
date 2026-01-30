import { create } from "zustand";

// Auth Store
export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem("access_token") || null,
  isAuthenticated: !!localStorage.getItem("access_token"),

  setUser: (user) => set({ user }),
  setToken: (token) => {
    localStorage.setItem("access_token", token);
    set({ token, isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    set({ user: null, token: null, isAuthenticated: false });
  },
}));

// UI Store
export const useUIStore = create((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  notifications: [],
  addNotification: (notification) =>
    set((state) => ({
      notifications: [...state.notifications, notification],
    })),
  removeNotification: (id) =>
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    })),
}));

// Clubs Store
export const useClubsStore = create((set) => ({
  clubs: [],
  selectedClub: null,
  setClubs: (clubs) => set({ clubs }),
  setSelectedClub: (club) => set({ selectedClub: club }),
}));

// Events Store
export const useEventsStore = create((set) => ({
  events: [],
  selectedEvent: null,
  setEvents: (events) => set({ events }),
  setSelectedEvent: (event) => set({ selectedEvent: event }),
}));
