import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Html5Qrcode } from "html5-qrcode";
import { scanQR } from "../../services/takeawayService";
import "./TakeawayQRScannerPage.css";

function TakeawayQRScannerPage() {
    const navigate = useNavigate();
    const scannerRef = useRef(null);
    const scannerRunningRef = useRef(false);
    const isProcessingRef = useRef(false);
    const [scanning, setScanning] = useState(false);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    useEffect(() => {
        scannerRef.current = new Html5Qrcode("qr-reader");

        return () => {
            if (scannerRef.current && scannerRunningRef.current) {
                scannerRef.current
                .stop()
                .catch(() => {})
                .finally(() => {scannerRunningRef.current = false});
            }
        };
    }, []);

    async function startScanner() {
        const scanner = scannerRef.current;
        if (!scanner || scannerRunningRef.current) {
            return;
        }
        setError("");
        setMessage("");
        setScanning(true);
        isProcessingRef.current = false;

        try {
            await scanner.start(
                { facingMode: "environment" },
                {
                    fps: 10,
                    qrbox: {
                        width: 250,
                        height: 250,
                    },
                },
                async (decodedText) => {
                    if (isProcessingRef.current) {
                        return;
                    }

                    isProcessingRef.current = true;

                    setMessage("QR scanned. Verifying...");
                    setScanning(false);

                    try {
                        await scanner.stop();
                        scannerRunningRef.current = false;

                        const response = await scanQR(decodedText);

                        const orderData = response.data.data;

                        navigate(`/takeaway/order-verification/${orderData.order_id}`);
                    } catch (error) {
                        const errorMessage = error.response?.data?.message || "Unable to scan QR code.";
                        setError(errorMessage);
                        setMessage("");
                        isProcessingRef.current = false;
                    }
                },
                () => {}
            );
            scannerRunningRef.current = true;
        } catch (error) {
            console.error("Unable to start scanner:", error);
            setScanning(false);
            scannerRunningRef.current = false;
            setError("Unable to access the camera. Please allow camera permission.");
        }
    }

    async function stopScanner() {
        const scanner = scannerRef.current;
        if (!scanner || !scannerRunningRef.current) {
            return;
        }
        try {
            await scanner.stop();
        } catch (error) {
            console.log("Scanner already stopped.");
        } finally {
            scannerRunningRef.current = false;
            setScanning(false);
        }
    }

    // return (
    //     <main className="pickup-page">
    //         <h1>Pickup QR Scanner</h1>

    //         <button onClick={() => navigate("/takeaway")}>
    //             Back to Dashboard
    //         </button>
    //         <br />
    //         <p>
    //             Scan the customer's pickup QR code to continue the
    //             verification process.
    //         </p>

    //         {message && <p>{message}</p>}

    //         {error && <p>{error}</p>}

    //         {!scanning && (
    //             <button onClick={startScanner}>
    //                 Scan QR
    //             </button>
    //         )}

    //         {scanning && (
    //             <button onClick={stopScanner}>
    //                 Stop Scanner
    //             </button>
    //         )}

    //         <div
    //             id="qr-reader"
    //             style={{
    //                 width: "100%",
    //                 maxWidth: "350px",
    //                 height: "260px",
    //                 margin: "20px auto",
    //                 overflow: "hidden",
    //             }}
    //         />
    //     </main>
    // );

    return (
        <main className="pickup-page">
            {/* Header */}
            <header className="pickup-header">
                <button className="back-button" onClick={() => navigate("/takeaway")}
                    aria-label="Back">
                    ←
                </button>

                <div>
                    <h1 style={{color:"black"}}>Pickup</h1>
                    <span style={{color:"black"}}>Order verification</span>
                </div>
            </header>

            {/* Main Card */}
            <section className="scanner-card">
                <div className="scanner-icon">
                    <span>⌁</span>
                </div>

                <h2 style={{color:"black"}}>Scan pickup QR</h2>

                <p className="scanner-description">
                    Scan the customer's QR code to verify their pickup order.
                </p>

                {/* Scanner */}
                <div className={`scanner-wrapper ${scanning ? "active" : ""}`}>
                    <div
                        id="qr-reader"
                        className="qr-reader"
                    />

                    {!scanning && (
                        <div className="scanner-placeholder">
                            <div className="qr-frame">
                                <span className="corner top-left"></span>
                                <span className="corner top-right"></span>
                                <span className="corner bottom-left"></span>
                                <span className="corner bottom-right"></span>

                                <div className="qr-placeholder-icon">
                                    ▦
                                </div>
                            </div>

                            <p>Ready to scan</p>
                        </div>
                    )}

                    {scanning && (
                        <div className="scan-line"></div>
                    )}
                </div>

                {/* Status */}
                {message && (
                    <div className="status-message success">
                        <span className="status-dot"></span>
                        {message}
                    </div>
                )}

                {error && (
                    <div className="status-message error">
                        <span>!</span>
                        {error}
                    </div>
                )}

                {/* Action */}
                <div className="scanner-actions">
                    {!scanning ? (
                        <button className="scan-button" onClick={startScanner}>
                            <span className="scan-button-icon">▦</span>
                            Scan QR Code
                        </button>
                    ) : (
                        <button className="stop-button" onClick={stopScanner}>
                            Stop Scanner
                        </button>
                    )}
                </div>

                {/* Instructions */}
                <div className="scan-tips">
                    <div className="tip">
                        <span className="tip-icon">☀</span>
                        <div>
                            <strong>Good lighting</strong>
                            <p>Make sure the QR code is clearly visible.</p>
                        </div>
                    </div>

                    <div className="tip">
                        <span className="tip-icon">◎</span>
                        <div>
                            <strong>Keep it steady</strong>
                            <p>Place the QR code inside the scanning frame.</p>
                        </div>
                    </div>
                </div>
            </section>

            <p className="footer-text" style={{color:"black"}}>
                Fast & secure pickup verification
            </p>
        </main>
    );

}

export default TakeawayQRScannerPage;
