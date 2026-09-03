import axiosInstance from "../api/axiosInstance";

async function getProducts() {
  const response = await axiosInstance.get("/products/all/");
  return response.data;
}

async function getProductById(productId) {
  const response = await axiosInstance.get(`/products/${productId}/`);
  return response.data;
}

export {getProducts,getProductById};