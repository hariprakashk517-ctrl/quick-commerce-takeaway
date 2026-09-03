import axiosInstance from "../api/axiosInstance";

export function createOrder(orderData) {
  return axiosInstance.post("/orders/create/",orderData);}

export function getCustomerOrders() {
  return axiosInstance.get("/orders/all/");}

export function getCustomerOrder(orderId) {
  return axiosInstance.get(`/orders/${orderId}/`);}

export function getPickupCredentials(orderId) {
  return axiosInstance.get(`/orders/${orderId}/pickup-credentials/`)}

export function refreshPickupCredentials(orderId) {
  return axiosInstance.post(`orders/${orderId}/refresh-pickup-credentials/`)}

export function markOutForPickup(orderId) {
    return axiosInstance.post(`/orders/${orderId}/out-for-pickup/`)}