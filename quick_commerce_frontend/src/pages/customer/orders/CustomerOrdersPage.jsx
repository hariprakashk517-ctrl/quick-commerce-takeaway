import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./CustomerOrdersPage.css"
import CustomerAccountLayout from "../../../layouts/CustomerAccountLayout";
import { getCustomerOrders } from "../../../services/orderService";

function CustomerOrdersPage() {
  const navigate = useNavigate();

  const [orders, setOrders] =
    useState([]);

  const [isLoading, setIsLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    async function fetchOrders() {
      try {
        setIsLoading(true);
        setError("");

        const response =
          await getCustomerOrders();

        const orderData =
          response.data.data;

        setOrders(orderData);
      } catch (error) {
        const message =
          error.response?.data?.message ||
          "Unable to fetch orders.";

        setError(message);
      } finally {
        setIsLoading(false);
      }
    }

    fetchOrders();
  }, []);

  if (isLoading) {
    return <p>Loading orders...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <CustomerAccountLayout>
    <main className="orders-page">
        <section className="orders-header">
            <div className="orders-header-icon">◷</div>
            <div>
                <h1>My Orders</h1>
                <p>
                    Track and manage your recent orders.
                </p>
            </div>
        </section>
        {orders.length === 0 ? (
            <section className="orders-empty-card">
                <div className="orders-empty-icon">🛍</div>
                <h2>No orders yet</h2>
                <p>
                  You have not placed any orders yet.
                  Start shopping and your orders will
                  appear here.
                </p>
                <button className="start-shopping-button" onClick={() =>navigate("/customer/products")}>
                  Start Shopping
                </button>
            </section>
        ) : (
            <section className="orders-list">
                {orders.map((order) => (
                    <article className="order-card" key={order.id}>
                        <div className="order-card-header">
                            <div>
                                <span className="order-label">Order</span>
                                <h2>{order.order_id}</h2>
                            </div>
                            <span className={`order-status status-${order.order_status?.toLowerCase()}`}>
                              {order.order_status}
                            </span>
                        </div>
                        <div className="order-info-grid">
                            <div className="order-info-item">
                                <span className="order-info-label">Fulfilment</span>
                                <strong>{order.fulfillment_mode}</strong>
                            </div>
                            <div className="order-info-item">
                                <span className="order-info-label">Payment</span>
                                <strong>{order.payment_status}</strong>
                            </div>
                            <div className="order-info-item">
                                <span className="order-info-label">Refund</span>
                                <strong>{order.refund_status}</strong>
                            </div>
                            <div className="order-info-item">
                                <span className="order-info-label">Total</span>
                                <strong className="order-total">
                                    ₹{order.total_amount}
                                </strong>
                            </div>
                        </div>
                        <div className="order-card-footer">
                            <div className="order-date">
                                <span>Placed on</span>
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
                            <button className="view-order-button" onClick={() =>navigate(`/customer/orders/${order.order_id}`)}>
                              View Details<span>→</span>
                            </button>
                        </div>
                    </article>
                ))}
            </section>
        )}
    </main>
    </CustomerAccountLayout>
  );
}

export default CustomerOrdersPage;