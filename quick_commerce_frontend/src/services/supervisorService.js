import axiosInstance from "../api/axiosInstance";

export function getPendingReplacementRequests() {
    return axiosInstance.get("/orders/replacement-requests/");
}

export function getReplacementRequestDetail(replacementRequestId) {
    return axiosInstance.get(`/orders/replacement-requests/${replacementRequestId}/`);
}

export function approveReplacement(replacementRequestId, data) {
    return axiosInstance.post(`/orders/replacement-requests/${replacementRequestId}/approve/`, data)
}
export function rejectReplacement(replacementRequestId, data) {
    return axiosInstance.post(`/orders/replacement-requests/${replacementRequestId}/reject/`, data)
}