import axiosInstance from "../api/axiosInstance";

export function getAddresses() {
  return axiosInstance.get("/address/all/");
}

export function createAddress(addressData) {
  return axiosInstance.post("/address/all/", addressData);
}

export function getAddressById(addressId) {
  return axiosInstance.get(`/address/${addressId}/`);
}

export function updateAddress(addressId, addressData) {
  return axiosInstance.patch(`/address/${addressId}/`,addressData);
}

export function deleteAddress(addressId) {
  return axiosInstance.delete(`/address/${addressId}/`);
}

export function defaultAddress() {
  return axiosInstance.get("/address/default");
}

// export function defaultAddress() {
//     return axiosInstance.get("/address/default");
// }

// export { getAddresses, createAddress, getAddressById, updateAddress, deleteAddress};