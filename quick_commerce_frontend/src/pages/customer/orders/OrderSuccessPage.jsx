import { useLocation, useNavigate, useParams } from "react-router-dom";
import "./OrderSuccessPage.css";
import DashboardLayout from "../../../layouts/DashboardLayout";

function OrderSuccessPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { orderId } = useParams();

  const order = location.state?.order;

  const displayedOrderId =
    order?.order_id || orderId;

  return (
    <DashboardLayout>
    <main className="order-success-page">
        <section className="order-success-card">
            <div className="order-success-icon">✓</div>
            <h1>Order Placed Successfully</h1>
            <p className="order-success-description">Your order has been created successfully.</p>
            <div className="success-order-details">
                <div className="success-details-header">
                    <h2>Order Details</h2>
                </div>
                <div className="success-detail-row">
                    <span>Order ID</span>
                    <strong>{displayedOrderId} </strong>
                </div>
                {order && (
                    <>
                        <div className="success-detail-row">
                            <span>Status</span>
                            <strong className="success-status">{order.status}</strong>
                        </div>
                        <div className="success-detail-row">
                            <span>Payment Status</span>
                            <strong>{order.payment_status}</strong>
                        </div>
                        <div className="success-detail-row total-row">
                            <span>Total Amount</span>
                            <strong>₹{order.total_amount}</strong>
                        </div>
                    </>
                )}
            </div>
            <div className="order-success-actions">
                <button type="button" className="view-order-button" onClick={() => navigate(`/customer/orders/${displayedOrderId}`)}>
                    View Order
                    <span>→</span>
                </button>
                <button type="button" className="continue-shopping-button" onClick={() =>navigate("/customer/products")}>Continue Shopping</button>
            </div>
            <p className="order-success-footer">Thank you for shopping with us.</p>
        </section>
    </main>
    </DashboardLayout>
  );
}

export default OrderSuccessPage;