import { useEffect, useState } from "react";
import "./ProductListPage.css";
import DashboardLayout from "../../../layouts/DashboardLayout";
import ProductCard from "../../../components/product/ProductCard";
import { getProducts } from "../../../services/productService";
import { getCart } from "../../../services/cartService";

function ProductListPage() {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [cart, setCart] = useState(null);

  async function fetchProductsAndCart() {
      try {
        setIsLoading(true);
        setError("");

        const [productsResponse, cartResponse] = await Promise.all([getProducts(),getCart()])
        const productData = productsResponse.data || productsResponse;
        setProducts(productData);

        const cartData = cartResponse.data?.data || cartResponse.data || cartResponse;
        setCart(cartData); 

      } catch (requestError) {
        const backendMessage = requestError.response?.data?.message || "Unable to load products.";
        setError(backendMessage);

      } finally {
        setIsLoading(false);
      }
    }

  useEffect(() => {
    fetchProductsAndCart();
  }, []);

  function getCartQuantity(productId) {
    if(!cart.items) {
      return 0;
    }

    const cartItem = cart.items.find(
      (item) => item.product_id === productId
    );

    return cartItem ? cartItem.quantity : 0;
  }

  return (
    <DashboardLayout>
        <main className="products-page">
            <section className="products-top">
                <div>
                    <span className="products-eyebrow">
                        Quick Commerce
                    </span>
                    <h1>All Products</h1>
                    <p>
                        Fresh products delivered quickly to your doorstep.
                    </p>
                </div>

                {!isLoading && !error && (
                    <span className="products-count">
                        {products.length} products
                    </span>
                )}
            </section>
            {!isLoading && !error && products.length > 0 && (
                <section className="products-toolbar">
                    <button type="button" className="product-filter-button active">
                        All Products
                    </button>

                    <button type="button" className="product-filter-button">
                        Popular
                    </button>

                    <button type="button" className="product-filter-button">
                        Best Deals
                    </button>
                </section>
            )}
            {isLoading && (
                <section className="products-loading">
                    <div className="products-loading-spinner"></div>
                    <p>Loading products...</p>
                </section>
            )}
            {!isLoading && error && (
                <section className="products-error">
                    <div className="products-error-icon">
                        !
                    </div>
                    <h2>Unable to load products</h2>
                    <p>{error}</p>
                </section>
            )}
            {!isLoading && !error &&
                products.length === 0 && (
                    <section className="products-empty">
                        <div className="products-empty-icon">
                            🛍
                        </div>
                        <h2>No products available</h2>
                        <p>
                            There are currently no products available.
                            Please check again later.
                        </p>
                    </section>
                )}
            {!isLoading && !error &&
                products.length > 0 && (
                    <section className="products-grid">
                        {products.map((product) => (
                            <div key={product.product_id} className="product-grid-item">
                                <ProductCard product={product}
                                    cartQuantity={getCartQuantity(product.product_id)}
                                    onCartUpdate={fetchProductsAndCart}/>
                            </div>
                        ))}
                    </section>
                )}
        </main>
    </DashboardLayout>
  );
}

export default ProductListPage;