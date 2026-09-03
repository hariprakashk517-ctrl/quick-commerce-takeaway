import "./ProfilePage.css";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import CustomerAccountLayout from "../../layouts/CustomerAccountLayout";

function ProfilePage() {

    const navigate = useNavigate();
    const { user, role, } = useAuth()
     const handleLogout = () => {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("user");
        navigate("/");
    }

    return (
        <CustomerAccountLayout>
        <main className="profile-page">
            <section className="profile-container">
                <div className="profile-header">
                    <div className="profile-avatar">{user?.username ? user.username.charAt(0).toUpperCase() : "U"}</div>
                    <div>
                        <h1>My Profile</h1>
                        <p>Manage your account details</p>
                    </div>
                </div>
                <div className="profile-details">
                    <div className="profile-row">
                        <span className="profile-label">Username</span>
                        <span className="profile-value">{user?.username || "Unknown User"}</span>
                    </div>
                    <div className="profile-row">
                        <span className="profile-label">Role</span>
                        <span className="profile-value">{role || "No Role"}</span>
                    </div>
                </div>
                <button type="button" className="profile-logout-button" onClick={handleLogout}>Logout</button>
            </section>
        </main>
        </CustomerAccountLayout>
    );
}
export default ProfilePage;