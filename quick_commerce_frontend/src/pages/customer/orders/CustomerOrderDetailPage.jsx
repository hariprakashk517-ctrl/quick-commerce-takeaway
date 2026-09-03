import { useEffect, useState } from "react";
import {useNavigate,useParams,} from "react-router-dom";
import { getCustomerOrder } from "../../../services/orderService";
import "./CustomerOrderDetailPage.css";
import DashboardLayout from "../../../layouts/DashboardLayout";

function CustomerOrderDetailPage() {
  const navigate = useNavigate();
  const { orderId } = useParams();

  const [order, setOrder] =
    useState(null);

  const [isLoading, setIsLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    async function fetchOrder() {
      try {
        setIsLoading(true);
        setError("");

        const response =
          await getCustomerOrder(orderId);

        const orderData =
          response.data.data;

        setOrder(orderData);
      } catch (error) {
        const message =
          error.response?.data?.message ||
          "Unable to fetch order details.";

        setError(message);
      } finally {
        setIsLoading(false);
      }
    }

    fetchOrder();
  }, [orderId]);

  if (isLoading) {
    return <p>Loading order details...</p>;
  }

  if (error) {
    return (
      <main>
        <p>{error}</p>

        <button
          onClick={() =>
            navigate("/customer/orders")
          }
        >
          Back to Orders
        </button>
      </main>
    );
  }

  if (!order) {
    return <p>Order not found.</p>;
  }

  return (
    <DashboardLayout>
    <main className="order-details-page">
        <section className="order-details-header">
            <button type="button" className="order-back-button"
              onClick={() =>navigate("/customer/orders")}aria-label="Back to Orders">←
            </button>
            <div>
                <h1>Order Details</h1>
                <p>View your order and item details.</p>
            </div>
        </section>
        <section className="order-summary-card">
            <div className="order-summary-top">
                <div>
                    <span className="order-detail-label">Order ID</span>
                    <h2>{order.order_id}</h2>
                </div>
                <span className="order-detail-status">
                    {order.order_status}
                </span>
            </div>
            <div className="order-detail-grid">
                <div className="order-detail-item">
                    <span>Store</span>
                    <strong>{order.store_name}</strong>
                </div>
                <div className="order-detail-item">
                    <span>Fulfillment</span>
                    <strong>{order.fulfillment_mode}</strong>
                </div>
                <div className="order-detail-item">
                    <span>Payment</span>
                    <strong>{order.payment_status}</strong>
                </div>
                <div className="order-detail-item">
                    <span>Refund</span>
                    <strong>{order.refund_status}</strong>
                </div>
            </div>
            <div className="order-total-row">
                <span>Total Amount</span>
                <strong>₹{order.total_amount}</strong>
            </div>
            <div className="order-dates">
                <div>
                    <span>Created At</span>
                    <strong>
                        {new Date(
                            order.created_at
                        ).toLocaleString("en-IN", {
                            day: "2-digit",
                            month: "short",
                            year: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                            hour12: true,
                        })}
                    </strong>
                </div>
                <div>
                    <span>Updated At</span>
                    <strong>
                        {new Date(
                            order.updated_at
                        ).toLocaleString("en-IN", {
                            day: "2-digit",
                            month: "short",
                            year: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                            hour12: true,
                        })}
                    </strong>
                </div>
            </div>
        </section>
        {order.fulfillment_mode === "TAKEAWAY" && (
            <section className="pickup-credentials-card">
                <div className="pickup-credentials-icon">▦</div>
                <div className="pickup-credentials-content">
                    <h2>Pickup Credentials</h2>
                    <p>
                        View your pickup QR code and OTP
                        for order handover.
                    </p>
                </div>
                <button type="button" className="pickup-credentials-button"  onClick={() =>navigate(`/customer/orders/${order.order_id}/pickup-credentials`)}>
                  View QR & OTP
                  <span>→</span>
                </button>
            </section>
        )}
        <section className="order-items-section">
            <div className="order-items-header">
                <div>
                    <h2>Order Items</h2>
                    <p>
                        {order.items.length}{" "}
                        {order.items.length === 1 ? "item" : "items"}
                    </p>
                </div>
            </div>
            {order.items.length === 0 ? (
                <div className="no-items-card">
                    <div className="no-items-icon">🛍</div>
                    <p>No items found.</p>
                </div>
            ) : (
                <div className="order-items-list">
                    {order.items.map((item) => (
                        <article className="order-item-card" key={item.id}>
                            <div className="order-item-main">
                                <div className="order-item-icon">🛍</div>
                                <div className="order-item-name">
                                    <h3>{item.product_name}</h3>
                                    <span>{item.item_status}</span>
                                </div>
                            </div>
                            <div className="order-item-details">
                                <div>
                                    <span>Quantity</span>
                                    <strong>{item.quantity}</strong>
                                </div>
                                <div>
                                    <span>Unit Price</span>
                                    <strong>₹{item.unit_price}</strong>
                                </div>
                                <div>
                                    <span>Total</span>
                                    <strong className="item-total">₹{item.total_price}</strong>
                                </div>
                                <div>
                                    <span>Verified</span>
                                    <strong
                                        className={item.is_verified ? "verified" : "not-verified"}>
                                        {item.is_verified ? "Yes" : "No"}
                                    </strong>
                                </div>
                            </div>
                        </article>
                    ))}
                </div>
            )}
        </section>
    </main>
    </DashboardLayout>
  );
}

export default CustomerOrderDetailPage;