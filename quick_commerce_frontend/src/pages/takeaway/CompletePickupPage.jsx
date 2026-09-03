import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { completePickup } from "../../services/takeawayService";
import "./CompletePickupPage.css";

function CompletePickupPage() {
    const { orderId } = useParams();
    const navigate = useNavigate();

    const [processing, setProcessing] = useState(false);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const [completed, setCompleted] = useState(false);

    async function handleCompletePickup() {
        try {
            setProcessing(true);
            setError("");
            setMessage("");

            const response = await completePickup(orderId);

            setMessage(response.data.message);
            setCompleted(true);

        } catch (error) {
            setError(
                error.response?.data?.message ||
                "Unable to complete pickup."
            );
        } finally {
            setProcessing(false);
        }
    }

    if (completed) {
        return (
            <main className="complete-pickup-page">
                <section className="complete-pickup-card completed-card">
                    <div className="complete-pickup-icon">
                        ✓
                    </div>
                    <h1>Pickup Completed</h1>
                    <p className="success-message">
                        {message || "Pickup completed successfully."}
                    </p>
                    <div className="pickup-order">
                        <span>Order ID</span>
                        <strong>{orderId}</strong>
                    </div>
                    <button className="complete-pickup-primary-button" onClick={() => navigate("/takeaway")}>
                        Go to Takeaway Dashboard
                    </button>

                </section>
            </main>
        );
    }

    return (
        <main className="complete-pickup-page">
            <section className="complete-pickup-card">
                <div className="complete-pickup-icon">
                    ✓
                </div>
                <h1>Complete Pickup</h1>
                <p className="complete-pickup-description">
                    OTP has been verified successfully.
                    Confirm below to complete the customer's pickup.
                </p>
                <div className="pickup-order">
                    <span>Order ID</span>
                    <strong>{orderId}</strong>
                </div>
                <div className="pickup-checks">
                    <p>✓ Payment completed</p>
                    <p>✓ OTP verified</p>
                    <p>✓ Order ready for final handover</p>
                </div>
                {error && (
                    <div className="pickup-status pickup-error">
                        <span>!</span>
                        <p>{error}</p>
                    </div>
                )}
                <button className="complete-pickup-primary-button" disabled={processing} onClick={handleCompletePickup}>
                    {processing ? "Completing Pickup..." : "Complete Pickup"}
                </button>

            </section>
        </main>
    );
}

export default CompletePickupPage;