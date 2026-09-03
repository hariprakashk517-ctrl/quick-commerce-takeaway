import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginPage.css";
import { loginUser } from "../../services/authService";
import { useAuth } from "../../context/AuthContext";

function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setIsLoading(true);

    try {
      const response = await loginUser(formData);

      const authData = response.data || response;

      login(authData);

      const userRole = authData.user?.role;

      const roleRoutes = {
        CUSTOMER: "/customer/products",
        PACKER: "/packer",
        TAKEAWAY_STAFF: "/takeaway",
        SUPERVISOR: "/supervisor",
        ADMIN: "/admin",
      };

      const dashboardRoute = roleRoutes[userRole];

      if (dashboardRoute) {
        navigate(dashboardRoute);
      } else {
        setError("Dashboard routing is not configured for this role.");
      }

    } catch (requestError) {
      const backendMessage =
        requestError.response?.data?.message ||
        "Unable to log in. Please check your credentials.";

      setError(backendMessage);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="login-page">
        <div className="login-container">
            <h1>Login</h1>

            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">Username</label>

                    <input
                        id="username"
                        type="text"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div>
                    <label htmlFor="password">Password</label>

                    <input
                        id="password"
                        type="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>

                {error && <p>{error}</p>}

                <button type="submit" disabled={isLoading}>
                    {isLoading ? "Logging in..." : "Login"}
                </button>
            </form>
        </div>
    </div>
  );
}

export default LoginPage;