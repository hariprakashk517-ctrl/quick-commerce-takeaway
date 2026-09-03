import { useEffect,useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { verifyPickupOTP,getPickupStatus } from "../../services/takeawayService";
import "./VerifyPickupOTPPage.css";

function VerifyPickupOTPPage() {
    const { orderId } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [otp, setOtp] = useState("");
    const [processing, setProcessing] = useState(false);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const [verified, setVerified] = useState(false);

    async function handleVerifyOTP() {
        try {
            setError("");
            setMessage("");

            if (otp.length !== 4) {
                setError("Please enter a valid 4-digit OTP.");
                return;
            }

            setProcessing(true);

            const response = await verifyPickupOTP(
                orderId,
                otp
            );

            setMessage(response.data.message);
            setVerified(true);

        } catch (error) {
            setError(
                error.response?.data?.message ||
                "Unable to verify OTP."
            );
        } finally {
            setProcessing(false);
        }
    }

    useEffect(() => {
        async function loadPickupStatus() {
            try {
                setLoading(true);
                setError("");

                const response = await getPickupStatus(orderId);

                const data = response.data.data;

                if (data.pickup_verified) {
                    setVerified(true);
                    setMessage("OTP verified successfully.");
                }

            } catch (error) {
                setError(
                    error.response?.data?.message ||
                    "Unable to fetch pickup status."
                );
            } finally {
                setLoading(false);
            }
        }

        loadPickupStatus();
    }, [orderId]);

    if (loading) {
        return (
            <main className="otp-page">
                <section className="otp-card">
                    <h1>OTP Verification</h1>
                    <p>Loading pickup status...</p>
                </section>
            </main>
        );
    }

    if (verified) {
        return (
            <main className="otp-page">
                <section className="otp-card otp-success-card">
                    <div className="otp-icon success-icon">
                        ✓
                    </div>
                    <h1>OTP Verification</h1>
                    <p className="otp-message success-message">
                        {message || "OTP verified successfully."}
                    </p>
                    <button className="otp-primary-button" onClick={() => navigate(`/takeaway/complete-pickup/${orderId}`)}>
                        Complete Pickup
                    </button>
                </section>
            </main>
        );
    }


    return (
        <main className="otp-page">
            <section className="otp-card">
                <div className="otp-icon">
                    #
                </div>

                <h1>OTP Verification</h1>

                <p className="otp-description">
                    Enter the 4-digit OTP provided by the customer
                    to complete the pickup verification.
                </p>

                <div className="otp-order">
                    <span>Order ID</span>
                    <strong>{orderId}</strong>
                </div>

                <div className="otp-form">
                    <label htmlFor="otp">
                        Enter 4-digit OTP
                    </label>

                    <input
                        id="otp"
                        className="otp-input"
                        type="text"
                        value={otp}
                        maxLength={4}
                        inputMode="numeric"
                        autoComplete="one-time-code"
                        placeholder="••••"
                        onChange={(event) => {
                            const value = event.target.value
                                .replace(/\D/g, "");

                            setOtp(value);
                        }}
                    />
                </div>

                {error && (
                    <div className="otp-status otp-error">
                        <span>!</span>
                        <p>{error}</p>
                    </div>
                )}

                {message && (
                    <div className="otp-status otp-success">
                        <span>✓</span>
                        <p>{message}</p>
                    </div>
                )}

                <button className="otp-primary-button" disabled={processing || otp.length !== 4} onClick={handleVerifyOTP}>
                    {processing ? "Verifying..." : "Verify OTP"}
                </button>

                <p className="otp-footer">
                    Enter the OTP carefully to complete the pickup.
                </p>

                {/* <button className="otp-primary-button" disabled={!verified}
                    onClick={() => navigate(`/takeaway/complete-pickup/${orderId}`)}>
                    Complete Pickup
                </button> */}

            </section>
        </main>
    );
}

export default VerifyPickupOTPPage;