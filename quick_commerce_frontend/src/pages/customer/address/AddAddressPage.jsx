import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../../../layouts/DashboardLayout";
import AddressForm from "../../../components/address/AddressForm";
import { createAddress } from "../../../services/addressService";


function AddAddressPage() {
  const navigate = useNavigate();

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleCreateAddress(formData) {
    try {
      setIsLoading(true);
      setError("");

      await createAddress(formData);

      navigate("/customer/addresses");
    } catch (requestError) {
      const backendMessage =
        requestError.response?.data?.message ||
        "Unable to create address.";

      setError(backendMessage);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <DashboardLayout>
        <main className="add-address-page">
            <section className="add-address-container">
                {error && (
                    <div className="address-error">
                      <span className="error-icon">!</span>
                      <p>{error}</p>
                    </div>
                )}
                <AddressForm onSubmit={handleCreateAddress} isLoading={isLoading}/>
            </section>
        </main>
    </DashboardLayout>
  );
}

export default AddAddressPage;