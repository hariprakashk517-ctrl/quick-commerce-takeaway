import { useState } from "react";
import { registerUser } from "../../services/authService";
import { Link } from "react-router-dom";
import "./RegisterPage.css";

function RegisterPage() {

  const [formData, setFormData] = useState({
    full_name: "",
    username: "",
    email: "",
    phone_number: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState("");

  const passwordsMatch =
  formData.password &&
  formData.confirm_password &&
  formData.password === formData.confirm_password;

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleRegistration = async (event) => {
    event.preventDefault();
    if (formData.password !== formData.confirm_password) {
      setError("Passwords do not match.");
      return;
    }
    setError("");
    setSuccess("");

    if (!formData.full_name.trim()) {
        setError("Full name is required.");
        return;
    }

    if (!formData.username.trim()) {
        setError("Username is required.");
        return;
    }

    if (!formData.email.trim()) {
        setError("Email is required.");
        return;
    }

    if (!formData.phone_number.trim()) {
        setError("Phone number is required.");
        return;
    }

    if (!/^\d{10}$/.test(formData.phone_number)) {
        setError("Phone number must be exactly 10 digits.");
        return;
    }

    if (formData.password.length < 8) {
        setError("Password must be at least 8 characters.");
        return;
    }

    if (formData.password !== formData.confirm_password) {
        setError("Passwords do not match.");
        return;
    }

    setIsLoading(true);

    const userData = {
      full_name: formData.full_name,
      username: formData.username,
      email: formData.email,
      phone_number: formData.phone_number,
      password: formData.password,
    };

    try {
      const response = await registerUser(userData);
       if (response.success) {
        setSuccess(response.message);
        setError("");

        setFormData({
          full_name: "",
          username: "",
          email: "",
          phone_number: "",
          password: "",
          confirm_password: "",
        });
      } else {
        setError(response.message || "Registration failed.");
      }
    } catch (error) {
        const backendMessage = error.response?.data?.message || "Unable to register. Please try again.";
        setError(backendMessage);
    }finally {
      setIsLoading(false);
    }
  };

  return (
  <div className="register-page">
    <div className="register-container" id="register-container">

      <h1 className="register-title">Register</h1>

      {error && (
        <p className="register-error" id="register-error">
          {error}
        </p>
      )}

      {success && (
        <p className="register-success" id="register-success">
          {success}
        </p>
      )}

      <form
        className="register-form"
        id="register-form"
        onSubmit={handleRegistration}
      >

        <div className="form-group" id="full-name-group">
          <label htmlFor="full_name">Full Name</label>
          <input
            type="text"
            id="full_name"
            name="full_name"
            value={formData.full_name}
            onChange={handleChange}
            placeholder="Enter your full name"
          />
        </div>

        <div className="form-group" id="username-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Enter your username"
          />
        </div>

        <div className="form-group" id="email-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email"
          />
        </div>

        <div className="form-group" id="phone-group">
          <label htmlFor="phone_number">Phone Number</label>
          <input
            type="tel"
            id="phone_number"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            placeholder="Enter your phone number"
          />
        </div>

        <div className="form-group" id="password-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
          />
        </div>

        <div className="form-group" id="confirm-password-group">
          <label htmlFor="confirm_password">Confirm Password</label>
          <input
            type="password"
            id="confirm_password"
            name="confirm_password"
            value={formData.confirm_password}
            onChange={handleChange}
            placeholder="Confirm your password"
          />
          {formData.confirm_password && (
            <p
              className={passwordsMatch ? "password-match success" : "password-match error"}>
              {passwordsMatch ? "✓ Passwords match" : "✕ Passwords do not match"}</p>
          )}
        </div>

        <button type="submit" className="register-button" id="register-button" disabled={isLoading}>
          {isLoading ? "Registering..." : "Register"}
        </button>

        <div className="login-link" id="login-link">
          Already have an account? <Link to="/">Login</Link>
        </div>

      </form>
    </div>
  </div>
);
}

export default RegisterPage;