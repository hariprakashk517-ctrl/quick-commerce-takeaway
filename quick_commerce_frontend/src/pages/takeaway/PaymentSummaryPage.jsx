import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {getPaymentSummary,collectPayment,} from "../../services/takeawayService";
import "./PaymentSummaryPage.css";

function PaymentSummaryPage() {
    const navigate = useNavigate();
    const { orderId } = useParams();
    const [summary, setSummary] = useState(null);
    const [paymentType, setPaymentType] = useState("");
    const [transactionId, setTransactionId] = useState("");
    const [loading, setLoading] = useState(true);
    const [processing, setProcessing] = useState(false);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    async function loadPaymentSummary() {
        try {
            setLoading(true);
            setError("");

            const response = await getPaymentSummary(orderId);

            const data = response.data.data;

            setSummary(data);

            setPaymentType(data.payment_type || "");

        } catch (error) {
            setError(
                error.response?.data?.message ||
                "Unable to fetch payment summary."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadPaymentSummary();
    }, [orderId]);

    async function handleCollectPayment() {
        try {
            setProcessing(true);
            setError("");
            setMessage("");

            const response = await collectPayment(
                orderId,
                {
                    payment_type: paymentType,
                    transaction_id: transactionId,
                }
            );

            setMessage(response.data.message);
            setSummary((previous) => ({
                ...previous,
                payment_status: response.data.data.payment_status,
            }));

        } catch (error) {
            setError(
                error.response?.data?.message || "Unable to collect payment."
            );
        } finally {
            setProcessing(false);
        }
    }

    if (loading) {
        return <p>Loading payment summary...</p>;
    }

    if (error && !summary) {
        return (
            <main>
                <p>{error}</p>

                <button onClick={() => navigate(-1)}>
                    Back
                </button>
            </main>
        );
    }

    if (!summary) {
        return <p>Payment summary not found.</p>;
    }

    const requiresTransactionId =
        paymentType === "UPI_ON_PICKUP" ||
        paymentType === "CARD_ON_PICKUP";

    const canCollect =
        summary.payment_status !== "PAID" &&
        paymentType &&
        (!requiresTransactionId || transactionId.trim());

    return (
        <main className="payment-summary-page">
            <section className="payment-summary-container">
                <div className="payment-summary-header">
                    <div>
                        <h1>Payment Summary</h1>
                        <p>Review the order and collect payment.</p>
                    </div>

                    <div className="payment-header-icon">₹</div>
                </div>

                {message && (
                    <div className="payment-message success">
                        <span>✓</span>
                        <p>{message}</p>
                    </div>
                )}

                {error && (
                    <div className="payment-message error">
                        <span>!</span>
                        <p>{error}</p>
                    </div>
                )}

                <section className="payment-section">
                    <div className="section-heading">
                        <span className="section-icon">▣</span>
                        <h2>Order Details</h2>
                    </div>

                    <div className="order-summary-list">
                        <div className="summary-row">
                            <span>Order ID</span>
                            <strong>{summary.order_id}</strong>
                        </div>

                        <div className="summary-row">
                            <span>Total Amount</span>
                            <strong className="total-amount">
                                ₹{summary.total_amount}
                            </strong>
                        </div>

                        <div className="summary-row">
                            <span>Payment Status</span>

                            <span className={`payment-status ${summary.payment_status === "PAID" ? "paid" : "pending"}`}>
                                {summary.payment_status}
                            </span>
                        </div>

                        <div className="summary-row">
                            <span>Verification</span>

                            <span className={`verification-status ${summary.verification_completed ? "completed" : "pending"}`}>
                                {summary.verification_completed ? "Completed" : "Pending"}
                            </span>
                        </div>
                    </div>
                </section>

                <section className="payment-section">
                    <div className="section-heading">
                        <span className="section-icon">₹</span>
                        <h2>Payment</h2>
                    </div>

                    <div className="payment-form">
                        <label htmlFor="payment-type">
                            Payment Method
                        </label>

                        <select
                            id="payment-type"
                            className="payment-select"
                            value={paymentType}
                            onChange={(e) => setPaymentType(e.target.value)}
                            disabled={processing || summary.payment_status === "PAID"}>
                            
                            <option value="">
                                Select Payment Method
                            </option>

                            <option value="CASH_ON_PICKUP">
                                Cash on Pickup
                            </option>

                            <option value="UPI_ON_PICKUP">
                                UPI on Pickup
                            </option>

                            <option value="CARD_ON_PICKUP">
                                Card on Pickup
                            </option>
                        </select>

                        {requiresTransactionId && (
                            <div className="transaction-field">
                                <label htmlFor="transaction-id">
                                    Transaction ID
                                </label>

                                <input
                                    id="transaction-id"
                                    className="payment-input"
                                    type="text"
                                    value={transactionId}
                                    onChange={(e) => setTransactionId(e.target.value)}
                                    placeholder="Enter transaction ID"
                                    disabled={processing}
                                />
                            </div>
                        )}

                        <button className="collect-payment-button" disabled={!canCollect || processing} onClick={handleCollectPayment}>
                            {processing ? "Processing..." : "Collect Payment"}
                        </button>
                    </div>
                </section>

                <button type="button" className="verify-otp-button" disabled={summary.payment_status !== "PAID"}
                    onClick={() => navigate(`/takeaway/verify-otp/${orderId}`)}>
                    Verify OTP
                </button>
            </section>
        </main>
    );
}

export default PaymentSummaryPage;