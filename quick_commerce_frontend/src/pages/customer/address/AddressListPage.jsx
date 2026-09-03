import { useEffect, useState } from "react";
import CustomerAccountLayout from "../../../layouts/CustomerAccountLayout";
import { getAddresses, deleteAddress } from "../../../services/addressService";
import { Link } from "react-router-dom";
import "./AddressListPage.css";

function AddressListPage() {
  const [addresses, setAddresses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchAddresses() {
      try {
        const response = await getAddresses();

        const addressData = response.data.data;

        setAddresses(addressData);
      } catch (requestError) {
        const backendMessage =
          requestError.response?.data?.message ||
          "Unable to load addresses.";

        setError(backendMessage);
      } finally {
        setIsLoading(false);
      }
    }

    fetchAddresses();
  }, []);

  async function handleDeleteAddress(addressId) {
  const confirmed = window.confirm(
    "Are you sure you want to delete this address?"
  );

  if (!confirmed) {
    return;
  }

  try {
    await deleteAddress(addressId);

    setAddresses((previousAddresses) =>
      previousAddresses.filter(
        (address) => address.id !== addressId
      )
    );
  } catch (requestError) {
    const backendMessage =
      requestError.response?.data?.message ||
      "Unable to delete address.";

    alert(backendMessage);
  }
}

  return (
    <CustomerAccountLayout>
        <main className="addresses-page">
            <section className="addresses-container">
                {/* Header */}
                <div className="addresses-header">
                    <div>
                        <h1>My Addresses</h1>
                        <p>Manage your saved delivery addresses.</p>
                    </div>
                    <Link to="/customer/addresses/add" className="add-address-button">
                        <span>+</span>
                        Add Address
                    </Link>
                </div>
                {/* Loading */}
                {isLoading && (
                    <div className="addresses-status loading-status">
                        <span className="loading-spinner"></span>
                        <p>Loading addresses...</p>
                    </div>
                )}
                {/* Error */}
                {error && (
                    <div className="addresses-status error-status">
                        <span className="error-icon">!</span>
                        <p>{error}</p>
                    </div>
                )}
                {/* Empty */}
                {!isLoading &&
                    !error &&
                    addresses.length === 0 && (
                        <div className="empty-addresses">
                            <div className="empty-address-icon"> ⌂ </div>
                            <h2>No addresses found</h2>
                            <p>Add your delivery address to make checkout faster and easier.</p>
                            <Link to="/customer/addresses/add" className="empty-add-button">Add Your First Address</Link>
                        </div>
                    )
                }
                {/* Address List */}
                {!isLoading &&
                    !error &&
                    addresses.length > 0 && (
                        <div className="address-list">
                            {addresses.map((address) => (
                                <article
                                    className={`address-card ${
                                      address.is_default ? "default-address-card" : "" }`} key={address.id}>
                                    {/* Card Header */}
                                    <div className="address-card-header">
                                        <div className="address-type">
                                            <span className="address-type-icon">
                                                {address.address_type === "HOME" ? "⌂" : address.address_type === "WORK" ? "▣" : "⌖"}
                                            </span>
                                            <div>
                                              <h3>{address.address_type}</h3>
                                              <span>Delivery Address</span>
                                            </div>
                                        </div>
                                        {/* Badges */}
                                        <div className="address-badges">
                                            {address.is_default && (
                                                <span className="address-badge default-badge">Default</span>
                                            )}
                                            {address.last_used && (
                                                <span className="address-badge last-used-badge">Last Used</span>
                                            )}
                                        </div>
                                    </div>
                                    {/* Address */}
                                    <div className="address-details">
                                        <p className="full-address">{address.full_address}</p>
                                        {/* Store */}
                                        <div className="address-info-row">
                                          <span className="info-label">Store</span>
                                          <span className="info-value">{address.selected_store_name || "Not assigned"}</span>
                                        </div>
                                        {/* Distance */}
                                        <div className="address-info-row">
                                          <span className="info-label">Distance</span>
                                            <span className="info-value">
                                              {address.distance_from_store_km ? `${address.distance_from_store_km} km` : "Not available"}
                                            </span>
                                        </div>
                                    </div>
                                    {/* Actions */}
                                    <div className="address-actions">
                                      <Link to={`/customer/addresses/${address.id}/edit`} className="edit-address-button">Edit</Link>
                                      <button type="button" className="delete-address-button" onClick={() =>handleDeleteAddress(address.id)}>Delete</button>
                                    </div>
                                </article>
                            ))}
                        </div>
                    )}
            </section>
        </main>
     </CustomerAccountLayout>
  );
}

export default AddressListPage;