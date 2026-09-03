import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPendingReplacementRequests } from "../../services/supervisorService";
import "./ReplacementRequestPage.css";

function ReplacementRequestsPage() {
    const navigate = useNavigate();

    const [requests, setRequests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    async function loadRequests() {
        try {
            setLoading(true);
            setError("");

            const response = await getPendingReplacementRequests();

            setRequests(response.data.data);
        } catch (error) {
            setError(
                error.response?.data?.message ||
                "Unable to fetch replacement requests."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadRequests();
    }, []);

    if (loading) {
        return <p>Loading replacement requests...</p>;
    }

    return (
        <main className="replacement-requests-page">
            <section className="replacement-requests-container">
                <div className="replacement-requests-header">
                    <div>
                        <h1>Pending Replacement Requests</h1>
                        <p>Review and manage customer replacement requests.</p>
                    </div>
                    <div className="replacement-header-icon">↻</div>
                </div>

                {error && (
                    <div className="replacement-error">
                        <span>!</span>
                        <p>{error}</p>
                    </div>
                )}

                {requests.length === 0 ? (
                    <div className="replacement-empty">
                        <div className="empty-icon">✓</div>
                        <h2>No pending requests</h2>
                        <p>There are currently no replacement requests waiting for approval.</p>
                    </div>
                ) : (
                    <div className="replacement-table-wrapper">
                        <table className="replacement-table">
                            <thead>
                                <tr>
                                    <th>Order ID</th>
                                    <th>Product</th>
                                    <th>Quantity</th>
                                    <th>Reason</th>
                                    <th>Status</th>
                                    <th>Action</th>
                                </tr>
                            </thead>

                            <tbody>
                                {requests.map((request) => (
                                    <tr key={request.id}>
                                        <td data-label="Order ID">
                                            <strong>{request.order_id}</strong>
                                        </td>

                                        <td data-label="Product">
                                            {request.product_name}
                                        </td>

                                        <td data-label="Quantity">
                                            <span className="quantity-badge">
                                                {request.quantity}
                                            </span>
                                        </td>

                                        <td data-label="Reason">
                                            {request.reason}
                                        </td>

                                        <td data-label="Status">
                                            <span className="pending-status">
                                                {request.status}
                                            </span>
                                        </td>

                                        <td data-label="Action">
                                            <button
                                                type="button"
                                                className="view-request-button"
                                                onClick={() =>
                                                    navigate(
                                                        `/supervisor/replacement-requests/${request.id}`
                                                    )
                                                }
                                            >
                                                View Request
                                                <span>→</span>
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </section>
        </main>
    );
}

export default ReplacementRequestsPage;