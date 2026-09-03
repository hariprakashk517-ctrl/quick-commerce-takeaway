import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { QRCodeSVG } from "qrcode.react";
import { getPickupCredentials, refreshPickupCredentials } from "../../../services/orderService";
import CountdownTimer from "../../../components/common/CountdownTimer";
import { useRef } from "react";
import "./PickupCredentialsPage.css";
import DashboardLayout from "../../../layouts/DashboardLayout";

function PickupCredentialsPage() {
    const navigate = useNavigate();
    const {orderId} = useParams();
    const [credentials, setCredentials] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [error, setError] = useState("");
    const [message, steMessage] = useState("");
    const pollingRef = useRef(null);

    async function fetchCredentials() {
        try {
            setError("")
            const response = await getPickupCredentials(orderId);
            const credentialsData = response.data.data
            setCredentials(credentialsData)
            if (credentialsData.qr_scanned && credentialsData.otp_enabled && pollingRef.current) 
            {
            clearInterval(pollingRef.current);
            pollingRef.current = null;
            }
        } catch (error) {
            const errorMessage = error.response?.data?.message || "Unable to fetch pickup credentials.";

            setError(errorMessage)
        } 
    }

    useEffect(() => {
        async function loadCredentials() {
            try{
                setIsLoading(true);
                await fetchCredentials();
            } finally {
                setIsLoading(false);
            }
        } loadCredentials();
        pollingRef.current = setInterval(() => {
        fetchCredentials();}, 10000);
        return () => {
        if (pollingRef.current) {
            clearInterval(pollingRef.current);
        }};
    }, [orderId]);

    async function handleRefreshCredentials() {
        setError("");
        setIsRefreshing(true);
        steMessage("");

        try{
            const response = await refreshPickupCredentials(orderId);
            setError(response.data.message);
            await fetchCredentials();
        } catch (error) {
            const errorMessage = error.response?.data?.message || "Unable to refresh pickup credentials.";
            setError(errorMessage);
        } finally {
            setIsLoading(false)
        }
    }

    if(isLoading) {
        return ( <p>Loading pickup credentials...</p> )
    }

    if (error && !credentials) {
        return (
            <main className="pickup-page pickup-error-page">
                <section className="pickup-error-card">
                    <div className="pickup-error-icon">!</div>
                    <h1>Pickup credentials not found</h1>
                    <p className="pickup-error-message">{error}</p>
                    <button className="pickup-error-button" onClick={() => navigate(`/customer/orders/${orderId}`)}>
                    ← Back to Order
                    </button>
                </section>
            </main>
        );
    }

    if(!credentials) {
        return ( <p>Pickup credentials not found</p> );
    }

    return (
        <DashboardLayout>
        <main className="pickup-page">
            <header className="pickup-header">
                <button className="back-button" onClick={() => navigate(`/customer/orders/${orderId}`)} aria-label="Back">
                ←
                </button>
                <div>
                    <h1 style={{color:"black"}}>Pickup Credentials</h1>
                    <span style={{color:"black"}}>
                        Order ID: #{credentials.order_id}
                    </span>
                </div>
            </header>
            {message && (
                <div className="credential-message success">
                    <span className="message-icon">✓</span>
                    {message}
                </div>
            )}
            {error && (
                <div className="credential-message error">
                    <span className="message-icon">!</span>
                    {error}
                </div>
            )}
            <section className="credential-card">
                <div className="credential-card-header">
                    <div className="credential-icon qr-icon">
                        ▦
                    </div>
                    <div>
                        <h2>Pickup QR Code</h2>
                        <p>
                            Show this QR code to the takeaway staff
                        </p>
                    </div>
                </div>
                <div className="qr-display">
                    {credentials.qr_token ? (
                        <div className="qr-code-container">
                            <QRCodeSVG value={credentials.qr_token} size={220} title={`Pickup QR for ${credentials.order_id}`}/>
                        </div>
                    ) : (
                        <div className="credential-unavailable">
                            <span>⌁</span>
                            <p>QR token is not available</p>
                        </div>
                    )}
                </div>
                <div className="credential-status">
                    <div className="status-row">
                        <span>QR Status</span>
                        <strong
                            className={credentials.qr_scanned ? "status-badge scanned" : "status-badge pending"}>
                            <span className="status-dot"></span>
                            {credentials.qr_scanned ? "Scanned" : "Not Scanned"}
                        </strong>
                    </div>
                    <div className="status-row">
                        <span>QR Expires In</span>
                        <strong className="countdown">
                        <CountdownTimer expiryTime={credentials.qr_expires_at}/>
                        </strong>
                    </div>
                </div>
            </section>
            <section className="credential-card otp-card">
                <div className="credential-card-header">
                    <div className="credential-icon otp-icon">
                        #
                    </div>
                    <div>
                        <h2>Pickup OTP</h2>
                        <p>
                            Use this code during final handover
                        </p>
                    </div>
                </div>
                {credentials.otp ? (
                    <>
                        <div className="otp-display">
                            <span className="otp-label">
                                Your OTP
                            </span>
                            <strong className="otp-code">
                                {credentials.otp}
                            </strong>
                        </div>
                        <div className="otp-warning">
                            <span>🔒</span>
                            <p>
                            Share this OTP only with the takeaway staff during final handover.
                            </p>
                        </div>
                    </>
                ) : (
                    <div className="credential-unavailable otp-unavailable">
                        <span>🔐</span>
                        <p>
                        OTP will be available after the QR code is scanned and order verification is completed.
                        </p>
                    </div>
                )}

                <div className="credential-status">
                    <div className="status-row">
                        <span>OTP Status</span>
                        <strong className={credentials.otp?.enabled ? "status-badge enabled" : "status-badge pending"}>
                        <span className="status-dot"></span>
                        {credentials.otp?.enabled ? "Enabled" : "Not Enabled"}
                        </strong>
                    </div>
                    <div className="status-row">
                        <span>OTP Expires In</span>
                        <strong className="countdown">
                        <CountdownTimer expiryTime={credentials.otp_expires_at}/>
                        </strong>
                    </div>
                </div>
            </section>
            <section className="refresh-section">
                <button className="refresh-button" onClick={handleRefreshCredentials} disabled={isRefreshing}>
                    <span className={isRefreshing ? "refresh-icon spinning" : "refresh-icon"}>
                    ↻
                    </span>
                    {isRefreshing ? "Refreshing..." : "Refresh Pickup Credentials"}
                </button>
            </section>
            <p className="footer-text" style={{color:"black"}}>
                Keep your pickup credentials secure
            </p>
        </main>
        </DashboardLayout>
    );

}

export default PickupCredentialsPage;