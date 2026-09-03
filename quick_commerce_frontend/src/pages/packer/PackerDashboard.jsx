import DashboardLayout from "../../layouts/DashboardLayout";
import { useNavigate } from "react-router-dom";

function PackerDashboard() {
  const navigate = useNavigate();
  return (
     <DashboardLayout>
      <h1>Packer Dashboard</h1>
      <p>View and manage packing orders.</p>
      <button onClick={()=>navigate(`/packer/packing`)}>Move to Packing</button>
    </DashboardLayout>
  );
}

export default PackerDashboard;