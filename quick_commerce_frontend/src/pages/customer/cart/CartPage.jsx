import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./CartPage.css";
import DashboardLayout from "../../../layouts/DashboardLayout";
import { getCart, updateCartItem, removeCartItem, clearCart,} from "../../../services/cartService";

function CartPage() {
  const [cart, setCart] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
  }, []);

  async function fetchCart() {
    try {
      setError("");

      const response = await getCart();

      const cartData = response.data.data || response;

      setCart(cartData);
    } catch (error) {
      setError(
        error.response?.data?.message ||
          "Unable to fetch cart."
      );
    } finally {
      setIsLoading(false);
    }
  }

  async function handleUpdateQuantity(
    productId,
    quantity
    ) {
    try {
        await updateCartItem(productId, quantity);

        fetchCart();
    } catch (error) {
        alert(
        error.response?.data?.message ||
            "Unable to update quantity."
        );
    }
    }

    async function handleRemoveItem(productId) {
    try {
        await removeCartItem(productId);

        fetchCart();
    } catch (error) {
        alert(
        error.response?.data?.message ||
        "Unable to remove item."
        );
    }
    }

    async function handleClearCart() {
        const confirmed = window.confirm("Are you sure you want to clear your cart?");

        if (!confirmed) 
            return;

        try {
            await clearCart();
            fetchCart();
        } catch (error) {
            alert(error.response?.data?.message || "Unable to clear cart.");
        }
    }

  if (isLoading) {
    return (
      <DashboardLayout>
        <h2>Loading...</h2>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <h2>{error}</h2>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
        <main className="cart-page">
            <div className="cart-container">
                <header className="cart-header">
                    <div>
                        <h1>My Cart</h1>
                        <p>
                            Review your items before checkout.
                        </p>
                    </div>
                </header>
                {cart.items.length === 0 ? (
                    <section className="cart-card empty-cart">
                        <div className="empty-cart-icon">
                            🛒
                        </div>
                        <h2>Your cart is empty</h2>
                        <p>
                            Add some products to your cart
                            to get started.
                        </p>
                        <button className="continue-shopping-button"
                            onClick={() =>navigate("/customer/products")}>
                            Start Shopping
                        </button>
                    </section>
                ) : (
                    <>
                        <section className="cart-card">
                            <div className="cart-store-header">
                                <div>
                                    <span className="store-label">Store</span>
                                    <h2>{cart.store_name}</h2>
                                </div>
                                <button type="button" className="clear-cart-button"
                                  onClick={handleClearCart}>
                                  Clear Cart
                                </button>
                            </div>
                        </section>
                        <section className="cart-card cart-items">
                            <div className="cart-items-header">
                                <h2>Items</h2>
                                <span>
                                    {cart.items.length}{" "}
                                    {cart.items.length === 1 ? "item" : "items"}
                                </span>
                            </div>
                            {cart.items.map((item) => (
                                <article key={item.id}className="cart-item">
                                    <div className="cart-item-info">
                                        <h3>{item.product_name}</h3>
                                        <p className="cart-item-price">₹{item.price}</p>
                                    </div>
                                    <div className="quantity-control">
                                        <button type="button" className="quantity-button"
                                            onClick={() =>handleUpdateQuantity(item.product_id,item.quantity - 1)}
                                            disabled={item.quantity === 1}>
                                            -
                                        </button>
                                        <span className="quantity-value">{item.quantity}</span>
                                        <button type="button" className="quantity-button"
                                          onClick={() => {handleUpdateQuantity(item.product_id,item.quantity + 1);}}>
                                          +
                                        </button>
                                    </div>
                                    <div className="cart-item-right">
                                        <strong className="item-total">₹{item.total_price}</strong>
                                        <button type="button" className="remove-item-button"
                                          onClick={() =>handleRemoveItem(item.product_id)}>
                                          Remove
                                        </button>
                                    </div>
                                </article>
                            ))}
                        </section>
                          <section className="cart-card cart-summary">
                            <div className="summary-row">
                                <span>Subtotal</span>
                                <span>₹{cart.cart_total}</span>
                            </div>
                            <div className="summary-total">
                                <span>Cart Total</span>
                                <strong>₹{cart.cart_total}</strong>
                            </div>
                        </section>
                        <button type="button" className="checkout-button"
                          onClick={() =>navigate("/customer/checkout")}
                          disabled={cart.items.length === 0}>
                          Proceed to Checkout<span>→</span>
                        </button>
                    </>
                )}
            </div>
        </main>
    </DashboardLayout>
  );
}

export default CartPage;