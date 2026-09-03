import axiosInstance from "../api/axiosInstance";


export function getPackingDoneOrders() {
    return axiosInstance.get("/box/packing-done/");
}

export function assignBox(data) {
    return axiosInstance.post("/box/assign/", data);
}

export function boxAssignedOrders() {
    return axiosInstance.get("/box/box-assigned/");
}

export function scanQR(qrToken) {
    return axiosInstance.post("/orders/scan-qr/", {qr_token:qrToken,});
}

export function getOrderVerification(orderId) {
    return axiosInstance.get(`/orders/${orderId}/verification/`); 
} 

export function verifyOrderItem(orderId, itemId) {
    return axiosInstance.post(`/orders/${orderId}/items/${itemId}/verify/`); 
}

export function cancelOrderItem(orderId, itemId, reason) {
    return axiosInstance.post(`/orders/${orderId}/items/${itemId}/cancel/`, { reason,} ); 
} 

export function requestReplacement(orderId, itemId, data) { 
    return axiosInstance.post(`/orders/${orderId}/items/${itemId}/request-replacement/`, data ); 
}

export function completeItemVerification(orderId) { 
    return axiosInstance.post(`/orders/${orderId}/complete-verification/`); 
}

export function getPaymentSummary(orderId) {
    return axiosInstance.get(`/orders/${orderId}/payment-summary/`);
}

export  function collectPayment(orderId, data) {
    return axiosInstance.post(`/payment/${orderId}/collect/`, data);
}

export function verifyPickupOTP(orderId, otp) {
    return axiosInstance.post(`/orders/${orderId}/verify-otp/`, {otp,});
}

export function completePickup(orderId) {
    return axiosInstance.post(`/orders/${orderId}/complete-pickup/`);
}

export function getPickupStatus(orderId) {
    return axiosInstance.get(`/orders/${orderId}/pickup-status/`);
}