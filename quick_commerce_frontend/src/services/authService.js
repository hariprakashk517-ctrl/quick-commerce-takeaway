import axiosInstance from "../api/axiosInstance";

export async function loginUser(credentials) {
  const response = await axiosInstance.post("/auth/login/", credentials);
  return response.data.data;
}

export async function registerUser(userData) {
  const response = await axiosInstance.post("/auth/register/", userData);
  return response.data;
}