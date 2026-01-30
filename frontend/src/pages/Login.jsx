import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuthStore } from "../store";
import { authService } from "../services/authService";
import Button from "../components/common/Button";
import Input from "../components/common/Input";
import Card from "../components/common/Card";
import { FiMail, FiLock } from "react-icons/fi";
import toast from "react-hot-toast";

export default function Login() {
  const navigate = useNavigate();
  const { setUser, setToken } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await authService.login(
        formData.email,
        formData.password,
      );
      setToken(response.access);
      setUser(response.user);
      toast.success("Login successful!");
      navigate("/");
    } catch (error) {
      const errorData = error.response?.data;
      if (errorData?.email || errorData?.password) {
        setErrors(errorData);
      } else {
        toast.error(error.response?.data?.message || "Login failed");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_#1b1033_0%,_#0b0614_65%)] flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo & Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-extrabold bg-gradient-to-r from-purple-400 via-purple-500 to-purple-700 bg-clip-text text-transparent mb-2 drop-shadow-[0_0_20px_rgba(147,51,234,0.35)]">
            Campus Hub
          </h1>
          <p className="text-purple-300/60">
            Unified Campus Resource Management
          </p>
        </div>

        {/* Form Card */}
        <Card className="border border-purple-900/40 bg-[#12091f]/80 backdrop-blur-xl shadow-[0_0_0_1px_rgba(147,51,234,0.15),0_30px_60px_rgba(0,0,0,0.6)]">
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              error={errors.email?.[0]}
              placeholder="your@email.com"
              icon={FiMail}
              className="w-full px-4 py-2 rounded-lg bg-white text-black placeholder-gray-500 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />

            <Input
              label="Password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              error={errors.password?.[0]}
              placeholder="••••••••"
              icon={FiLock}
              className="w-full px-4 py-2 rounded-lg bg-white text-black placeholder-gray-500 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />

            <Button
              variant="primary"
              size="lg"
              className="w-full mt-6"
              disabled={loading}
              type="submit"
            >
              {loading ? "Signing in..." : "Sign In"}
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-dark-700">
            <p className="text-center text-gray-400">
              Don't have an account?{" "}
              <Link
                to="/register"
                className="text-primary-500 hover:text-primary-400 font-medium"
              >
                Sign up
              </Link>
            </p>
          </div>
        </Card>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>© 2024 Campus Management. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
}
