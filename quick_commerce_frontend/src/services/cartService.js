import axiosInstance from "../api/axiosInstance";

export function getCart() {
  return axiosInstance.get("/cart/detail/");
}

export function addCartItem(productId, quantity = 1) {
  return axiosInstance.post("/cart/add/", {
    product_id: productId,
    quantity: quantity,
  });
}

export function updateCartItem(productId, quantity) {
  return axiosInstance.patch("/cart/update/", {
    product_id: productId,
    quantity: quantity,
  });
}

export function removeCartItem(productId) {
  return axiosInstance.delete("/cart/remove/", {
    data: {
      product_id: productId,
    },
  });
}

export function clearCart() {
  return axiosInstance.delete("/cart/clear/");
}