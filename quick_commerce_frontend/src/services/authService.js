import axiosInstance from "../api/axiosInstance";

async function loginUser(credentials) {
  const response = await axiosInstance.post("/auth/login/", credentials);

  return response.data;
}

export { loginUser };