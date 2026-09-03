import { useNavigate } from "react-router-dom";
import "./TakeawayStaffLayout.css";

function TakeawayStaffLayout({ children }) {
    const navigate = useNavigate();

    return (
        <div className="takeaway-staff-layout">
            <header className="takeaway-staff-header">
                <div className="takeaway-brand">
                    <div className="takeaway-brand-icon">
                        🛍
                    </div>
                    <div>
                        <h2>Quick Commerce</h2>
                        <span>Takeaway Staff</span>
                    </div>
                </div>
                <button type="button" className="takeaway-profile-button"
                    onClick={() => navigate("/takeaway/profile")} aria-label="Open profile">
                    👤
                </button>
            </header>
            <main className="takeaway-staff-content">
                {children}
            </main>

        </div>
    );
}

export default TakeawayStaffLayout;