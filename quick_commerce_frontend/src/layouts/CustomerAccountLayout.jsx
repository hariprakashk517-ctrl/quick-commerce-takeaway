import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./CustomerAccountLayout.css";

function CustomerAccountLayout({ children }) {
    const navigate = useNavigate();
    const location = useLocation();

    const { user, role } = useAuth();

    const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("user");

        navigate("/");
    };

    const isActive = (path) => {
        return location.pathname === path;
    };

    const handleNavigation = (path) => {
        navigate(path);
    };

    return (
        <main className="customer-account-page">
            <section className="customer-account-container">
                <aside className="customer-account-sidebar">
                    <div className="account-user">
                        <div className="account-avatar">
                            {user?.username ? user.username.charAt(0).toUpperCase() : "U"}
                        </div>

                        <div className="account-user-info">
                            <h2>
                                {user?.username || "User"}
                            </h2>

                            <p>
                                {user?.phone || "Manage your account"}
                            </p>
                        </div>
                    </div>

                    <nav className="account-navigation">
                        <button type="button"
                            className={`account-nav-item ${isActive("/customer/orders") ? "active" : ""}`}
                            onClick={() =>handleNavigation("/customer/orders")}>
                            <span className="account-nav-icon">
                                🛍
                            </span>
                            <span>
                                Orders
                            </span>
                            <span className="account-nav-arrow">
                                ›
                            </span>
                        </button>

                        <button type="button"
                            className={`account-nav-item ${isActive("/customer/addresses") ? "active" : ""}`}
                            onClick={() =>handleNavigation("/customer/addresses")}>
                            <span className="account-nav-icon">
                                ⌖
                            </span>
                            <span>
                                Saved Addresses
                            </span>
                            <span className="account-nav-arrow">
                                ›
                            </span>
                        </button>

                        <button type="button"
                            className={`account-nav-item ${isActive("/profile") ? "active" : ""}`}
                            onClick={() =>handleNavigation("/profile")}>
                            <span className="account-nav-icon">
                                ◯
                            </span>
                            <span>
                                Profile
                            </span>
                            <span className="account-nav-arrow">
                                ›
                            </span>
                        </button>
                    </nav>

                    <div className="account-sidebar-footer">
                        <button type="button" className="account-logout-button" onClick={handleLogout}>
                            Logout
                        </button>
                    </div>
                </aside>
                <div className="customer-account-content">
                    {children}
                </div>
            </section>
        </main>
    );
}

export default CustomerAccountLayout;