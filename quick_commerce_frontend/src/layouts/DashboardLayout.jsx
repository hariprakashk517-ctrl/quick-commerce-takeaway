import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { defaultAddress } from "../services/addressService";
import "./DashboardLayout.css";

function DashboardLayout({ children }) {
  const navigate = useNavigate();
   const [selectedAddress, setSelectedAddress] = useState(null);

    useEffect(() => {
        loadDefaultAddress();
    }, []);

    async function loadDefaultAddress() {
        try {
            const response = await defaultAddress();

            if (response.data.success) {
                setSelectedAddress(response.data.data);
            } else {
                setSelectedAddress(null);
            }
        } catch (error) {
            console.error("Unable to load default address:", error);
            setSelectedAddress(null);
        }
    }

  return (
    <div className="dashboard-layout">    
        <header className="dashboard-header">
            <div className="dashboard-logo" onClick={() => navigate("/customer")}>Quick Commerce</div>
            <button type="button" className="selected-address" onClick={() => navigate("/customer/addresses")}>
                <span className="location-icon">⌖</span>
                <span className="selected-address-content">
                    <span className="selected-address-label">Deliver to</span>
                    <span className="selected-address-text">
                        {selectedAddress?.address_type || "Select Address"}
                    </span>
                </span>
                <span className="address-arrow">›</span>
            </button>
            <div className="dashboard-search">
                <span className="search-icon">⌕</span>
                <input type="text" placeholder="Search for products..."/>
            </div>
            <button type="button" className="header-icon-button" onClick={() => navigate("/customer/cart")} aria-label="Cart" title="Cart" >🛒</button>
            <button type="button" className="profile-icon-button" onClick={() => navigate("/profile")} aria-label="Profile" title="Profile">U</button>
        </header>
        <main className="dashboard-content">{children}</main>
    </div>
  );
}

export default DashboardLayout;

