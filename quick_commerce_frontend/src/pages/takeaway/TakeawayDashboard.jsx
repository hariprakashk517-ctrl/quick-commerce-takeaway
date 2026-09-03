// import DashboardLayout from "../../layouts/DashboardLayout";
import { useNavigate } from "react-router-dom";
import TakeawayStaffLayout from "../../layouts/TakeawayStaffLayout";
import "./TakeawayDashboard.css";

function TakeawayDashboard() {
  const navigate = useNavigate();
   return (
    <TakeawayStaffLayout>
      <main className="takeaway-dashboard-page">
          <section className="takeaway-dashboard-card">
              <div className="takeaway-dashboard-icon">
                  🛍
              </div>

              <h1>Takeaway Staff Dashboard</h1>

              <p className="takeaway-dashboard-description">
                  Manage box assignment and customer pickup.
              </p>

              <div className="takeaway-dashboard-actions">
                  <button className="takeaway-action-button" onClick={() =>navigate("/takeaway/box-assign")}>
                      <span className="takeaway-button-icon">▣</span>
                      Box Assign
                  </button>
                  <button className="takeaway-action-button" onClick={() =>navigate("/takeaway/box-assigned/")}>
                      <span className="takeaway-button-icon">□</span>
                      Box Assigned Orders
                  </button>
                  <button className="takeaway-action-button" onClick={() =>navigate("/takeaway/scan-qr")}>
                    <span className="takeaway-button-icon">▦</span>
                    Pickup QR Scanner
                  </button>
              </div>
          </section>
      </main>
      </TakeawayStaffLayout>
  );
}

export default TakeawayDashboard;