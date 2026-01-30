import { Link, useLocation } from "react-router-dom";
import {
  FiHome,
  FiUsers,
  FiCalendar,
  FiAward,
  FiBarChart2,
  FiSettings,
  FiX,
} from "react-icons/fi";
import { useUIStore, useAuthStore } from "../../store";
import clsx from "clsx";

const menuItems = [
  { icon: FiHome, label: "Dashboard", path: "/" },
  { icon: FiUsers, label: "Clubs", path: "/clubs" },
  { icon: FiCalendar, label: "Events", path: "/events" },
  { icon: FiAward, label: "Resources", path: "/resources" },
  { icon: FiBarChart2, label: "Analytics", path: "/analytics", admin: true },
  { icon: FiSettings, label: "Settings", path: "/settings" },
];

export default function Sidebar() {
  const location = useLocation();
  const { sidebarOpen, toggleSidebar } = useUIStore();
  const { user } = useAuthStore();

  return (
    <>
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={toggleSidebar}
        />
      )}

      <aside
        className={clsx(
          "fixed left-0 top-0 h-full w-64 bg-dark-800 border-r border-dark-700 z-50",
          "transform transition-transform duration-200 md:relative md:translate-x-0",
          sidebarOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="p-6 flex items-center justify-between">
          <h2 className="text-xl font-bold text-primary-500">Campus Hub</h2>
          <button
            onClick={toggleSidebar}
            className="md:hidden text-gray-400 hover:text-white"
          >
            <FiX size={20} />
          </button>
        </div>

        <nav className="mt-8 px-4 space-y-2">
          {menuItems.map((item) => {
            if (item.admin && user?.role !== "admin") return null;

            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                className={clsx(
                  "flex items-center gap-3 px-4 py-3 rounded-lg transition-all",
                  isActive
                    ? "bg-primary-600 text-white"
                    : "text-gray-300 hover:bg-dark-700",
                )}
                onClick={() => {
                  if (window.innerWidth < 768) toggleSidebar();
                }}
              >
                <Icon size={20} />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>
    </>
  );
}
