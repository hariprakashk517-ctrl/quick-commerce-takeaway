import DashboardLayout from "../../layouts/DashboardLayout";
import {useNavigate} from "react-router-dom"

function CustomerDashboard() {
  const navigate = useNavigate();

  // const handleLogout = () => {
  //   localStorage.removeItem("accessToken");
  //   localStorage.removeItem("refreshToken");
  //   localStorage.removeItem("user");
  //   navigate("/");
  // }
  return (
     <DashboardLayout>
      <h1>Customer Dashboard</h1>
      <p>Welcome to the customer section.</p>
      <button onClick={() =>navigate("/customer/orders")}>
      My Orders
      </button>
      {/* <button onClick={handleLogout}>Logout</button> */}
    </DashboardLayout>
  );
}

export default CustomerDashboard;