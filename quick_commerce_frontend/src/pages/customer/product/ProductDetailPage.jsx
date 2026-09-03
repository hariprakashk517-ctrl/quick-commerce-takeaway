import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import DashboardLayout from "../../../layouts/DashboardLayout";
import { getProductById } from "../../../services/productService";
import { addCartItem } from "../../../services/cartService";

function ProductDetailPage() {
  const { productId } = useParams();

  const [product, setProduct] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const [isAdding, setIsAdding] = useState(false);
  const [cartMessage, setCartMessage] = useState("");

  useEffect(() => {
    async function fetchProduct() {
      try {
        setError("");

        const response = await getProductById(productId);

        const productData = response.data || response;

        setProduct(productData);
      } catch (requestError) {
        const backendMessage =
          requestError.response?.data?.message ||
          "Unable to load product.";

        setError(backendMessage);
      } finally {
        setIsLoading(false);
      }
    }

    fetchProduct();
  }, [productId]);

  async function handleAddToCart() {
    try {
        setIsAdding(true);
        setCartMessage("");

        const response = await addCartItem(
        product.product_id,
        1
        );

        setCartMessage(response.data.message);
    } catch (error) {
        const message =
        error.response?.data?.message ||
        "Unable to add product to cart.";

        setCartMessage(message);
    } finally {
        setIsAdding(false);
    }
    }


  return (
    <DashboardLayout>
      {isLoading && <p>Loading product...</p>}

      {error && <p>{error}</p>}

      {!isLoading && !error && product && (
        <div>
          <h1>{product.product_name}</h1>

          <p>SKU: {product.sku}</p>

          <p>
            {product.description || "No description available."}
          </p>

          <p>Price: ₹{product.price}</p>

          <p>Store: {product.store_name}</p>

            <p>Stock Status: {product.stock_status}</p>

            <p>
            Availability: {product.in_stock ? "Available" : "Unavailable"}
            </p>

            {/* <button disabled={!product.can_add_to_cart}>
            {product.can_add_to_cart ? "Add to Cart" : "Unavailable"}
            </button> */}

            <button disabled={!product.can_add_to_cart || isAdding} onClick={handleAddToCart}>
                {isAdding ? "Adding..." : product.can_add_to_cart ? "Add to Cart" : "Unavailable"}
            </button>

            {cartMessage && <p>{cartMessage}</p>}

        </div>
      )}
    </DashboardLayout>
  );
}

export default ProductDetailPage;