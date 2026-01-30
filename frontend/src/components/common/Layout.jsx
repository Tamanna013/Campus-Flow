import { useAuthStore } from "../../store";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

export default function Layout({ children }) {
  const { isAuthenticated } = useAuthStore();

  if (!isAuthenticated) {
    return <main>{children}</main>;
  }

  return (
    <div className="flex h-screen bg-dark-900">
      <Sidebar />
      <div className="flex flex-col flex-1">
        <Navbar />
        <main className="flex-1 overflow-auto">
          <div className="p-6">{children}</div>
        </main>
      </div>
    </div>
  );
}
