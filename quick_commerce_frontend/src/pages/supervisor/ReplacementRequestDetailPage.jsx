import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {getReplacementRequestDetail,approveReplacement,rejectReplacement} from "../../services/supervisorService";
import "./ReplacementRequestDetailPage.css";

function ReplacementRequestDetailPage() {
    const navigate = useNavigate();
    const { replacementRequestId } = useParams();
    const [request, setRequest] = useState(null);
    const [history, setHistory] = useState([]);
    const [availableQuantity, setAvailableQuantity] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [processing, setProcessing] = useState(false);
    const [message, setMessage] = useState("");
    const [supervisorNote, setSupervisorNote] = useState("");

    async function loadRequest() {
        try {
            setLoading(true);
            setError("");
            const response = await getReplacementRequestDetail(replacementRequestId);
            const data = response.data.data;
            setRequest(data.current_request);
            setHistory(data.replacement_history);
            setAvailableQuantity(data.available_quantity);

        } catch (error) {
            setError(error.response?.data?.message || "Unable to fetch replacement request.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadRequest();
    }, [replacementRequestId]);

    async function handleApprove() {

         if (!supervisorNote.trim()) {
            setError("Supervisor note is required.");
            return;
        }

        try {
            setProcessing(true);
            setError("");
            setMessage("");

            const response = await approveReplacement(
                replacementRequestId,
                {
                    supervisor_note: supervisorNote.trim(),
                }
            );

            setMessage(response.data.message);
            navigate("/supervisor/replacement-requests");

        } catch (error) {
            setError(
                error.response?.data?.message || "Unable to approve replacement request."
            );
        } finally {
            setProcessing(false);
        }
    }

    async function handleReject() {

        if (!supervisorNote.trim()) {
            setError("Supervisor note is required.");
            return;
        }

        try {
            setProcessing(true);
            setError("");
            setMessage("");

            const response = await rejectReplacement(
                replacementRequestId,
                {
                    supervisor_note: supervisorNote.trim(),
                }
            );

            setMessage(response.data.message);
            navigate("/supervisor/replacement-requests");

        } catch (error) {
            setError(
                error.response?.data?.message || "Unable to reject replacement request."
            );
        } finally {
            setProcessing(false);
        }
    }

    if (loading) {
        return <p>Loading replacement request...</p>;
    }

    if (error) {
        return (
            <main>
                <p>{error}</p>
                <button onClick={() => navigate(-1)}>
                    Back
                </button>
            </main>
        );
    }

    if (!request) {
        return <p>Replacement request not found.</p>;
    }

    const canApprove = request.status === "PENDING" && availableQuantity >= request.quantity;

    return (
        <main className="replacement-page">
            <header className="replacement-header">
                <button type="button" className="replacement-back-button" onClick={() => navigate(-1)} aria-label="Back">
                    ←
                </button>
                <div>
                    <h1>Replacement Request</h1>
                    <p>Review and process the replacement request.</p>
                </div>
            </header>
            <section className="replacement-card">
                <div className="replacement-card-header">
                    <div className="replacement-icon">↻</div>
                    <div>
                        <h2>Request Details</h2>
                        <span>Replacement information</span>
                    </div>
                </div>
                <div className="replacement-details">
                    <div className="replacement-detail">
                        <span>Order ID</span>
                        <strong>{request.order_id}</strong>
                    </div>
                    <div className="replacement-detail">
                        <span>Product</span>
                        <strong>{request.product_name}</strong>
                    </div>
                    <div className="replacement-detail">
                        <span>Quantity</span>
                        <strong>{request.quantity}</strong>
                    </div>
                    <div className="replacement-detail">
                        <span>Reason</span>
                        <strong>{request.reason_display}</strong>
                    </div>
                    <div className="replacement-detail">
                        <span>Status</span>
                        <strong className="replacement-status">
                            {request.status_display}
                        </strong>
                    </div>
                    <div className="replacement-detail">
                        <span>Available Quantity</span>
                        <strong>{availableQuantity}</strong>
                    </div>
                </div>
            </section>
            <section className="replacement-card">
                <div className="replacement-section-header">
                    <div>
                        <h2>Replacement History</h2>
                        <p>Previous replacement activity for this request.</p>
                    </div>
                </div>
                {history.length === 0 ? (
                    <div className="replacement-empty">
                        <div className="empty-history-icon">↻</div>
                        <p>No replacement history.</p>
                    </div>
                ) : (
                    <div className="replacement-history-wrapper">
                        <table className="replacement-history-table">
                            <thead>
                                <tr>
                                    <th>Product</th>
                                    <th>Reason</th>
                                    <th>Status</th>
                                    <th>Created At</th>
                                </tr>
                            </thead>
                            <tbody>
                                {history.map((item) => (
                                    <tr key={item.id}>
                                        <td>
                                            {item.product_name}
                                        </td>
                                        <td>
                                            {item.reason_display || item.reason}
                                        </td>
                                        <td>
                                            <span className="history-status">
                                                {item.status_display || item.status}
                                            </span>
                                        </td>
                                        <td>{item.created_at}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </section>
            <section className="replacement-card decision-card">
                <div className="replacement-section-header">
                    <div>
                        <h2>Review Request</h2>
                        <p>
                            Add a note before approving or rejecting
                            this request.
                        </p>
                    </div>
                </div>
                <div className="supervisor-note-wrapper">
                    <label htmlFor="supervisor-note">Supervisor Note</label>
                    <textarea id="supervisor-note" value={supervisorNote}
                        onChange={(e) =>setSupervisorNote(e.target.value)}
                        placeholder="Enter reason for your decision..." rows="4"/>
                </div>
                {request.status === "PENDING" &&
                    availableQuantity < request.quantity && (
                        <div className="stock-warning">
                            <span>!</span>
                            <p>
                                Insufficient stock to approve this
                                replacement request.
                            </p>
                        </div>
                    )}
                <div className="replacement-actions">
                    <button type="button" className="approve-button"
                        disabled={!canApprove || processing || !supervisorNote.trim()}
                        onClick={handleApprove}>
                        {processing ? "Approving..." : "✓ Approve"}
                    </button>
                    <button type="button" className="reject-button"
                        disabled={request.status !== "PENDING" || processing || !supervisorNote.trim()}
                        onClick={handleReject}>
                        {processing ? "Processing..." : "✕ Reject"}
                    </button>
                </div>
                <button type="button" className="replacement-secondary-button" onClick={() => navigate(-1)}>
                    ← Back
                </button>
            </section>
        </main>
    );
}

export default ReplacementRequestDetailPage;