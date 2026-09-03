import axiosInstance from "../api/axiosInstance";

export function getPackingOrders() {
    return axiosInstance.get("/orders/packing/");
}

export function getPackingOrderById (orderId) {
    return axiosInstance.get(`/orders/${orderId}/packing/`);
}

export function startPacking(orderId) {
    return axiosInstance.post(`/orders/${orderId}/start-packing/`);
}

export function completePacking(orderId) {
    return axiosInstance.post(`/orders/${orderId}/complete-packing/`);
}