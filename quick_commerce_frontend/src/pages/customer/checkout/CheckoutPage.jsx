import { useEffect, useState } from "react";
import "./CheckoutPage.css";
import DashboardLayout from "../../../layouts/DashboardLayout";
import { getCart } from "../../../services/cartService";
import { getAddresses } from "../../../services/addressService";
import { useNavigate } from "react-router-dom";
import { createOrder } from "../../../services/orderService";

function CheckoutPage() {
  const [cart, setCart] = useState(null);
  const [selectedAddress, setSelectedAddress] = useState(null);
  const [fulfilmentMode, setFulfilmentMode] = useState("DELIVERY");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const [paymentType, setPaymentType] = useState("PREPAID");
  const [isSubmitting, setIsSubmitting] =useState(false);
  const [submitError, setSubmitError] =useState("");

  useEffect(() => {
    fetchCheckoutData();
  }, []);

    async function fetchCheckoutData() {
        try {
            setIsLoading(true);
            setError("");

            const [cartResponse, addressResponse] =
            await Promise.all([
                getCart(),
                getAddresses(),
            ]);

            const cartData = cartResponse.data.data;
            const addressData = addressResponse.data?.data || [];

            setCart(cartData);

            const selectedDeliveryAddress = addressData.find((address) => address.is_default) || addressData[0];

            setSelectedAddress(selectedDeliveryAddress || null);

        } catch (error) {
            const message =
            error.response?.data?.message ||
            error.message ||
            "Unable to load checkout details.";

            setError(message);
        } finally {
            setIsLoading(false);
        }
        }

  async function handlePlaceOrder() {
    try {
      setIsSubmitting(true);
      setSubmitError("");

      const orderData = {
        fulfillment_mode: fulfilmentMode,
        payment_type: paymentType,
      };

      const response =
        await createOrder(orderData);

      const createdOrder =
        response.data.data;

      navigate(
        `/customer/orders/${createdOrder.order_id}/success`,
        {
          state: {
            order: createdOrder,
          },
        }
      );
    } catch (error) {
      const message =
        error.response?.data?.message ||
        "Unable to create order.";

      setSubmitError(message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleFulfillmentModeChange(mode) {
    setFulfilmentMode(mode);

    if (mode === "DELIVERY") {
      setPaymentType("PREPAID");
    }
  }

  if (isLoading) {
    return (
      <DashboardLayout>
        <p>Loading checkout...</p>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <p>{error}</p>
      </DashboardLayout>
    );
  }

  if (!cart || cart.items.length === 0) {
    return (
      <DashboardLayout>
        <div>
          <h1>Checkout</h1>
          <p>Your cart is empty.</p>
        </div>
      </DashboardLayout>
    );
  }

   return (
        <DashboardLayout>
            <main className="checkout-page">
                <div className="checkout-container">
                    <header className="checkout-header">
                        <button type="button"className="checkout-back-button"onClick={() => navigate(-1)}aria-label="Back">
                            ←
                        </button>
                        <div>
                            <h1>Checkout</h1>
                            <p>Review your order before placing it.</p>
                        </div>
                    </header>
                    <section className="checkout-section">
                        <h2>Fulfilment Method</h2>
                        <label className="checkout-option">
                            <input type="radio" name="fulfilmentMode" value="DELIVERY"
                                checked={fulfilmentMode === "DELIVERY"}
                                onChange={(event) =>handleFulfillmentModeChange(event.target.value)}/>
                            <span>Delivery</span>
                        </label>
                        <label className="checkout-option">
                            <input type="radio" name="fulfilmentMode" value="TAKEAWAY"
                                checked={fulfilmentMode === "TAKEAWAY"}
                                onChange={(event) =>handleFulfillmentModeChange(event.target.value)}/>
                            <span>Takeaway</span>
                        </label>
                    </section>
                    <section className="checkout-section">
                        <h2>Payment Method</h2>
                        <label className="checkout-option">
                            <input type="radio" name="paymentType" value="PREPAID"
                                checked={paymentType === "PREPAID"}
                                onChange={(event) =>setPaymentType(event.target.value)}/>
                            <span>Prepaid</span>
                        </label>
                        {fulfilmentMode === "TAKEAWAY" && (
                            <>
                                {/* <label className="checkout-option">
                                    <input type="radio" name="paymentType" value="CASH_ON_PICKUP"
                                        checked={paymentType ==="CASH_ON_PICKUP"}
                                        onChange={(event) =>setPaymentType(event.target.value)}/>
                                    <span>Cash on Pickup</span>
                                </label> */}
                                <label className="checkout-option">
                                    <input type="radio" name="paymentType" value="PAY_AT_TAKEAWAY"
                                        checked={paymentType ==="PAY_AT_TAKEAWAY"}
                                        onChange={(event) =>setPaymentType(event.target.value)}/>
                                     <span>Pay at Takeaway</span>
                                </label>
                                {/* <label className="checkout-option">
                                    <input type="radio" name="paymentType" value="CARD_ON_PICKUP"
                                        checked={paymentType ==="CARD_ON_PICKUP"}
                                        onChange={(event) =>setPaymentType(event.target.value)}/>
                                    <span>Card on Pickup</span>
                                </label> */}
                            </>
                        )}
                    </section>
                    {fulfilmentMode === "DELIVERY" && (
                        <section className="checkout-section">
                            <h2>Delivery Address</h2>
                            {!selectedAddress ? (
                                <p className="no-address">
                                    Please add an address before
                                    checkout.
                                </p>
                            ) : (
                                <div className="delivery-address">
                                    <h3>{selectedAddress.address_type}</h3>
                                    <p>{selectedAddress.full_address}</p>
                                </div>
                            )}
                        </section>
                    )}
                    {fulfilmentMode === "TAKEAWAY" && (
                        <section className="checkout-section">
                            <h2>Pickup Store</h2>
                            <div className="pickup-store">
                                <p>{cart.store_name}</p>
                                <p>{cart.store_address}</p>
                            </div>
                        </section>
                    )}
                    <section className="checkout-section">
                        <h2>Order Items</h2>
                        {cart.items.map((item) => (
                            <div key={item.id} className="checkout-item">
                                <h3>{item.product_name}</h3>
                                <p>Price: ₹{item.price}</p>
                                <p>Quantity: {item.quantity}</p>
                                <p>Total: ₹{item.total_price}</p>
                            </div>
                        ))}
                    </section>
                    <section className="checkout-section payment-summary">
                        <h2>Payment Summary</h2>
                        <div className="summary-row">
                            <span>Subtotal</span>
                            <span>₹{cart.cart_total}</span>
                        </div>
                        <div className="summary-total">
                            <span>Total Amount</span>
                            <span>₹{cart.cart_total}</span>
                        </div>
                    </section>
                    <button type="button" className="place-order-button"
                        onClick={handlePlaceOrder}
                        disabled={isSubmitting || !paymentType ||
                            (fulfilmentMode === "DELIVERY" && !selectedAddress)}>
                        {isSubmitting ? "Placing Order..." : "Place Order"}
                    </button>
                    {submitError && (
                        <p className="checkout-error">{submitError}</p>
                    )}
                </div>
            </main>
        </DashboardLayout>
    );
}

export default CheckoutPage;