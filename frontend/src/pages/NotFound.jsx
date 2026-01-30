import { Link } from "react-router-dom";
import Button from "../components/common/Button";
import { FiArrowLeft } from "react-icons/fi";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 to-dark-800 flex items-center justify-center px-4">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-primary-500 mb-2">404</h1>
        <p className="text-2xl font-bold text-white mb-2">Page Not Found</p>
        <p className="text-gray-400 mb-8">
          The page you're looking for doesn't exist.
        </p>

        <Link to="/">
          <Button variant="primary" size="lg">
            <FiArrowLeft className="inline mr-2" />
            Go Home
          </Button>
        </Link>
      </div>
    </div>
  );
}
