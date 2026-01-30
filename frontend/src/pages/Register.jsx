import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authService } from "../services/authService";
import Button from "../components/common/Button";
import Input from "../components/common/Input";
import Card from "../components/common/Card";
import toast from "react-hot-toast";

export default function Register() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    password_confirm: "",
    department: "",
    year: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Client-side validation
    if (formData.password !== formData.password_confirm) {
      setErrors({ password_confirm: "Passwords do not match" });
      setLoading(false);
      return;
    }

    try {
      await authService.register(formData);
      toast.success(
        "Registration successful! Please check your email to verify.",
      );
      navigate("/login");
    } catch (error) {
      const errorData = error.response?.data;
      setErrors(errorData || { general: "Registration failed" });
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
          <p className="text-purple-300/60">Create your account</p>
        </div>

        {/* Form Card */}
        <Card className="border border-purple-900/40 bg-[#12091f]/80 backdrop-blur-xl shadow-[0_0_0_1px_rgba(147,51,234,0.15),0_30px_60px_rgba(0,0,0,0.6)]">
          <form onSubmit={handleSubmit} className="space-y-4">
            {errors.general && (
              <div className="bg-red-600/20 border border-red-600 text-red-400 px-4 py-3 rounded-lg">
                {errors.general}
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <Input
                label="First Name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                error={errors.first_name?.[0]}
                placeholder="John"
                className="w-full px-4 py-2 rounded-lg bg-white text-black placeholder-gray-500 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <Input
                label="Last Name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                error={errors.last_name?.[0]}
                placeholder="Doe"
                className="w-full px-4 py-2 rounded-lg bg-white text-black placeholder-gray-500 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            <Input
              label="Email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              error={errors.email?.[0]}
              placeholder="your@email.com"
              className="w-full px-4 py-2 rounded-lg bg-white text-black placeholder-gray-500 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />

            <Input
              label="Department"
              name="department"
              value={formData.department}
              onChange={handleChange}
              error={errors.department?.[0]}
              placeholder="Computer Science"
              className="w-full px-4 py-2 rounded-lg bg-white text-black placeholder-gray-500 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Year
                </label>
                <select
                  name="year"
                  value={formData.year}
                  onChange={handleChange}
                  className="input-field"
                >
                  <option value="">Select Year</option>
                  <option value="1st">1st Year</option>
                  <option value="2nd">2nd Year</option>
                  <option value="3rd">3rd Year</option>
                  <option value="4th">4th Year</option>
                </select>
              </div>
            </div>

            <Input
              label="Password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              error={errors.password?.[0]}
              placeholder="••••••••"
              className="w-full px-4 py-2 rounded-lg bg-white text-black placeholder-gray-500 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />

            <Input
              label="Confirm Password"
              type="password"
              name="password_confirm"
              value={formData.password_confirm}
              onChange={handleChange}
              error={errors.password_confirm}
              placeholder="••••••••"
              className="w-full px-4 py-2 rounded-lg bg-white text-black placeholder-gray-500 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />

            <Button
              variant="primary"
              size="lg"
              className="w-full mt-6"
              disabled={loading}
              type="submit"
            >
              {loading ? "Creating account..." : "Create Account"}
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-dark-700">
            <p className="text-center text-gray-400">
              Already have an account?{" "}
              <Link
                to="/login"
                className="text-primary-500 hover:text-primary-400 font-medium"
              >
                Sign in
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}
