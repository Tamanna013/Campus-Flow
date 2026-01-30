import { FiBell, FiUser, FiLogOut, FiMenu } from "react-icons/fi";
import { useAuthStore, useUIStore } from "../../store";
import Button from "./Button";
import { Link } from "react-router-dom";

export default function Navbar() {
  const { user, logout } = useAuthStore();
  const { toggleSidebar } = useUIStore();

  return (
    <nav className="bg-dark-800 border-b border-dark-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <button
          onClick={toggleSidebar}
          className="text-gray-400 hover:text-white md:hidden"
        >
          <FiMenu size={24} />
        </button>

        <div className="flex-1 text-center">
          <h1 className="text-2xl font-bold text-primary-500">Campus Hub</h1>
        </div>

        <div className="flex items-center gap-4">
          <button className="text-gray-400 hover:text-primary-500 transition-colors">
            <FiBell size={20} />
          </button>

          <div className="flex items-center gap-3">
            <img
              src={user?.profile_picture || "https://via.placeholder.com/40"}
              alt={user?.first_name}
              className="w-10 h-10 rounded-full border border-primary-600"
            />
            <div className="hidden sm:block">
              <p className="text-sm font-medium text-gray-200">
                {user?.first_name}
              </p>
              <p className="text-xs text-gray-400">{user?.role}</p>
            </div>
          </div>

          <button
            onClick={logout}
            className="text-gray-400 hover:text-red-400 transition-colors"
          >
            <FiLogOut size={20} />
          </button>
        </div>
      </div>
    </nav>
  );
}
