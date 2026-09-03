import { useState } from "react";
import "./AddressForm.css"

function AddressForm({ initialData, onSubmit, isLoading }) {
  const [formData, setFormData] = useState({
    address_type: initialData?.address_type || "HOME",
    full_address: initialData?.full_address || "",
    latitude: initialData?.latitude || "",
    longitude: initialData?.longitude || "",
    is_default: initialData?.is_default || false,
  });

  function handleChange(event) {
    const { name, value, type, checked } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit(formData);
  }

  return (
    <main className="address-page">
        <section className="address-container">
            <div className="address-header">
                <h1>Add Address</h1>
                <p>Save your delivery address for faster checkout.</p>
            </div>
            <form onSubmit={handleSubmit} className="address-form">
                <div className="form-group">
                    <label htmlFor="address_type">
                        Address Type
                    </label>
                    <select id="address_type" name="address_type" value={formData.address_type} onChange={handleChange}>
                        <option value="HOME">Home</option>
                        <option value="WORK">Work</option>
                        <option value="OTHER">Other</option>
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="full_address">
                        Full Address
                    </label>
                    <textarea id="full_address" name="full_address" value={formData.full_address} onChange={handleChange} required placeholder="Enter your complete address"/>
                </div>
                <div className="location-row">
                    <div className="form-group">
                        <label htmlFor="latitude">
                            Latitude
                        </label>
                        <input id="latitude" type="number" step="any" name="latitude" value={formData.latitude} onChange={handleChange} required placeholder="Latitude" />
                    </div>
                    <div className="form-group">
                        <label htmlFor="longitude">
                            Longitude
                        </label>
                        <input id="longitude" type="number" step="any" name="longitude" value={formData.longitude} onChange={handleChange} required placeholder="Longitude" />
                    </div>
                </div>
                <label className="default-address">
                    <input type="checkbox" name="is_default" checked={formData.is_default} onChange={handleChange}/>
                    <span className="custom-checkbox"></span>
                    <span>
                        Set as default address
                    </span>
                </label>
                <button type="submit" className="save-address-button" disabled={isLoading}>
                    <span className="save-button-icon">
                        {isLoading ? "↻" : "✓"}
                    </span>
                    <span>
                        {isLoading ? "Saving..." : "Save Address"}
                    </span>
                </button>
            </form>
        </section>
    </main>
  );
}

export default AddressForm;