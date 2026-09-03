import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import DashboardLayout from "../../../layouts/DashboardLayout";
import AddressForm from "../../../components/address/AddressForm";
import {getAddressById,updateAddress} from "../../../services/addressService";

function EditAddressPage() {
  const { addressId } = useParams();
  const navigate = useNavigate();

  const [address, setAddress] = useState(null);
  const [isLoadingAddress, setIsLoadingAddress] = useState(true);
  const [isUpdating, setIsUpdating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchAddress() {
      try {
        setError("");

        const response = await getAddressById(addressId);

        const addressData = response.data || response;

        setAddress(addressData);
      } catch (requestError) {
        const backendMessage =
          requestError.response?.data?.message ||
          "Unable to load address.";

        setError(backendMessage);
      } finally {
        setIsLoadingAddress(false);
      }
    }

    fetchAddress();
  }, [addressId]);

  async function handleUpdateAddress(formData) {
    try {
      setIsUpdating(true);
      setError("");

      await updateAddress(addressId, formData);

      navigate("/customer/addresses");
    } catch (requestError) {
      const backendMessage =
        requestError.response?.data?.message ||
        "Unable to update address.";

      setError(backendMessage);
    } finally {
      setIsUpdating(false);
    }
  }

  return (
    <DashboardLayout>
      {/* <h1>Edit Address</h1> */}

      {error && <p>{error}</p>}

      {isLoadingAddress && <p>Loading address...</p>}

      {!isLoadingAddress && address && (
        <AddressForm
          initialData={address}
          onSubmit={handleUpdateAddress}
          isLoading={isUpdating}
        />
      )}
    </DashboardLayout>
  );
}

export default EditAddressPage;