import axiosInstance from "../api/axiosInstance";

export async function loginUser(credentials) {
  const response = await axiosInstance.post("/auth/login/", credentials);
  return response.data.data;
}

export function registerUser(userData) {
  return axiosInstance.post("/auth/register/", userData);
}