import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./TakeawayOrderVerificationPage.css";
import {getOrderVerification,verifyOrderItem,cancelOrderItem,requestReplacement,completeItemVerification,} from "../../services/takeawayService";


const cancellationReasons = [
    {value: "WRONG_ITEM", label: "Wrong Item Packed",},
    {value: "DAMAGED_ITEM", label: "Damaged Item",},
    {value: "ITEM_MISSING", label: "Item Missing",},
    {value: "CUSTOMER_DECLINED", label: "Customer Declined Item",},
    {value: "QUALITY_ISSUE", label: "Quality Issue",},
    {value: "OTHER", label: "Other",},
];

const replacementReasons = [
    { value: "DAMAGED_ITEM", label: "Damaged Item" },
    { value: "WRONG_ITEM", label: "Wrong Item Packed" },
    { value: "QUALITY_ISSUE", label: "Quality Issue" },
    { value: "PACKAGING_DAMAGE", label: "Packaging Damage" },
    { value: "ITEM_MISSING", label: "Item Missing" },
    { value: "OTHER", label: "Other" },
];

function TakeawayOrderVerificationPage() {
    const { orderId } = useParams();
    const navigate = useNavigate();
    const [order, setOrder] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const [processingItemId, setProcessingItemId] = useState(null);
    const [cancelItemId, setCancelItemId] = useState(null);
    const [cancelReason, setCancelReason] = useState("");
    const [replacementItemId, setReplacementItemId] = useState(null);
    const [replacementReason, setReplacementReason] = useState("");
    const [isRequestingReplacement, setIsRequestingReplacement] = useState(false);

    async function fetchOrderVerification() {
        try {
            setError("");
            const response = await getOrderVerification(orderId);
            setOrder(response.data.data);
        } catch (error) {
            const errorMessage = error.response?.data?.message || "Unable to load order verification.";
            setError(errorMessage);
        }
    }

    useEffect(() => {
        async function loadOrder() {
            setIsLoading(true);
            await fetchOrderVerification();
            setIsLoading(false);
        }
        loadOrder();
    }, [orderId]);

    async function handleVerifyItem(itemId) {
        try {
            setProcessingItemId(itemId);
            setError("");
            setMessage("");
            const response = await verifyOrderItem(orderId, itemId);
            setMessage(response.data.message);
            setOrder((previousOrder) => ({
                ...previousOrder,
                items: previousOrder.items.map((item) =>
                    item.id === itemId
                        ? {
                            ...item,
                            is_verified: true,
                        }: item
                ),
            }));
        } catch (error) {
            const errorMessage =
                error.response?.data?.message ||
                "Unable to verify item.";

            setError(errorMessage);
        } finally {
            setProcessingItemId(null);
        }
    }

    async function handleCancelItem() {
        if (!cancelItemId) {
            return;
        }

        if (!cancelReason.trim()) {
            setError("Cancellation reason is required.");
            return;
        }

        try {
            setProcessingItemId(cancelItemId);
            setError("");
            setMessage("");
            const response = await cancelOrderItem(orderId,cancelItemId,cancelReason);
            setMessage(response.data.message);
            setOrder((previousOrder) => ({
                ...previousOrder,
                items: previousOrder.items.map((item) =>
                    item.id === cancelItemId
                        ? {
                            ...item,
                            item_status: "CANCELLED",
                            is_verified: false,
                        }
                        : item
                ),
            }));
            setCancelItemId(null);
            setCancelReason("");
        } catch (error) {
            const errorMessage = error.response?.data?.message || "Unable to cancel item.";
            setError(errorMessage);
        } finally {
            setProcessingItemId(null);
        }
    }

    function handleRequestReplacement(itemId) {
        setReplacementItemId(itemId);
        setReplacementReason("");
    }

    async function handleConfirmReplacement() {
        if (!replacementReason) {
            return;
        }
        setIsRequestingReplacement(true);
        try {
            const response = await requestReplacement(
                orderId,
                replacementItemId,
                {
                    reason: replacementReason,
                }
            );
            console.log(response.data);
            setReplacementItemId(null);
            setReplacementReason("");
            await fetchOrderVerification();
        } catch (error) {
            console.log("Replacement error:", error.response?.data);
            const errorMessage = error.response?.data?.message || "Unable to request replacement.";
            setError(errorMessage);
        } finally {
            setIsRequestingReplacement(false);
        }
    }

    async function handleCompleteVerification() {
        try {
            setError("");
            setMessage("");
            setProcessingItemId("complete");

            const response = await completeItemVerification(orderId);

            setMessage(response.data.message);
            const status = response.data.data.status;
            const paymentStatus = response.data.data.payment_status;
            
            if (status === "PAYMENT_PENDING") {
                navigate(`/takeaway/payment-summary/${orderId}`);
                return;
            }

            if (status === "READY_FOR_FINAL_HANDOVER" && paymentStatus === "PAID") {
                navigate(`/takeaway/verify-otp/${orderId}`);
                return;
            }
            await fetchOrderVerification();
        } catch (error) {
            const errorMessage = error.response?.data?.message || "Unable to complete item verification.";
            setError(errorMessage);
        } finally {
            setProcessingItemId(null);
        }
    }

    if (isLoading) {
        return <p>Loading order verification...</p>;
    }

    if (error && !order) {
        return (
            <main>
                <h1>Order Verification</h1>
                <p>{error}</p>
                <button onClick={() => navigate("/takeaway")}>
                Back to Dashboard
                </button>
            </main>
        );
    }

    if (!order) {
        return <p>Order verification details not found.</p>;
    }

    const hasPendingItems = order.items.some((item) => item.item_status === "ACTIVE" && !item.is_verified);
    const hasPendingReplacement = order.order_status === "REPLACEMENT_PENDING_APPROVAL";

    return (
        <main className="order-verification-page">
            <header className="verification-header">
                <div className="verification-header-icon">✓</div>
                <div>
                    <h1>Order Verification</h1>
                    <p>Verify items before completing the pickup</p>
                </div>
            </header>

            <section className="verification-summary">
                <div className="summary-item">
                    <span>Order ID</span>
                    <strong>{order.order_id}</strong>
                </div>
                <div className="summary-item">
                    <span>Box</span>
                    <strong>{order.box_id}</strong>
                </div>
                <div className="summary-item">
                    <span>Status</span>
                    <strong className={`order-status status-${order.order_status?.toLowerCase()}`}>
                        {order.order_status}
                    </strong>
                </div>
            </section>

            {message && (
                <div className="verification-message success-message">
                    <span>✓</span>
                    <p>{message}</p>
                </div>
            )}

            {error && (
                <div className="verification-message error-message">
                    <span>!</span>
                    <p>{error}</p>
                </div>
            )}

            <section className="items-card">
                <div className="section-heading">
                    <div>
                        <h2>Order Items</h2>
                        <p>Verify each item before completing the order.</p>
                    </div>
                    <span className="item-count">{order.items.length}</span>
                </div>

                <div className="verification-items">
                    {order.items.map((item) => {
                        const isProcessing = processingItemId === item.id;
                        return (
                            <article
                                key={item.id}
                                className={`verification-item ${
                                    item.is_verified ? "item-verified" : ""
                                } ${
                                    item.item_status === "CANCELLED"
                                        ? "item-cancelled"
                                        : ""
                                }`}
                            >
                                <div className="item-top">
                                    <div className="item-product-icon">▦</div>

                                    <div className="item-product-info">
                                        <h3>{item.product_name}</h3>
                                        <p>Quantity: {item.quantity}</p>
                                    </div>

                                    <div className={`verification-badge ${
                                        item.is_verified
                                            ? "verified"
                                            : item.item_status === "CANCELLED"
                                            ? "cancelled"
                                            : "pending"
                                    }`}>
                                        {item.is_verified
                                            ? "Verified"
                                            : item.item_status === "CANCELLED"
                                            ? "Cancelled"
                                            : "Pending"}
                                    </div>
                                </div>

                                {item.item_status === "CANCELLED" && (
                                    <div className="item-notice cancelled-notice">
                                        This item has been cancelled.
                                    </div>
                                )}

                                {item.is_verified && (
                                    <div className="item-notice verified-notice">
                                        ✓ This item has been verified.
                                    </div>
                                )}

                                {item.item_status === "ACTIVE" && !item.is_verified && (
                                    <div className="item-actions">
                                        <button
                                            className="verify-item-button"
                                            onClick={() => handleVerifyItem(item.id)}
                                            disabled={
                                                item.is_verified ||
                                                processingItemId === item.id ||
                                                order?.order_status === "REPLACEMENT_PENDING_APPROVAL"
                                            }
                                        >
                                            {processingItemId === item.id
                                                ? "Verifying..."
                                                : "✓ Verify Item"}
                                        </button>

                                        <button
                                            className="cancel-item-button"
                                            onClick={() => {
                                                setCancelItemId(item.id);
                                                setCancelReason("");
                                                setError("");
                                            }}
                                            disabled={
                                                item.item_status !== "ACTIVE" ||
                                                item.is_verified ||
                                                processingItemId === item.id ||
                                                order?.order_status === "REPLACEMENT_PENDING_APPROVAL"
                                            }
                                        >
                                            Cancel Item
                                        </button>

                                        {cancelItemId === item.id && (
                                            <div className="action-panel cancel-panel">
                                                <h4>Cancel Item</h4>
                                                <p>Select a reason for cancelling this item.</p>

                                                <select
                                                    value={cancelReason}
                                                    onChange={(event) =>
                                                        setCancelReason(event.target.value)
                                                    }
                                                >
                                                    <option value="">
                                                        Select cancellation reason
                                                    </option>

                                                    {cancellationReasons.map((reason) => (
                                                        <option
                                                            key={reason.value}
                                                            value={reason.value}
                                                        >
                                                            {reason.label}
                                                        </option>
                                                    ))}
                                                </select>

                                                <div className="panel-actions">
                                                    <button
                                                        className="confirm-danger-button"
                                                        onClick={handleCancelItem}
                                                        disabled={processingItemId === item.id}
                                                    >
                                                        {processingItemId === item.id
                                                            ? "Cancelling..."
                                                            : "Confirm Cancel"}
                                                    </button>

                                                    <button
                                                        className="close-panel-button"
                                                        onClick={() => {
                                                            setCancelItemId(null);
                                                            setCancelReason("");
                                                        }}
                                                        disabled={processingItemId === item.id}
                                                    >
                                                        Close
                                                    </button>
                                                </div>
                                            </div>
                                        )}

                                        <button
                                            className="replacement-button"
                                            onClick={() => handleRequestReplacement(item.id)}
                                            disabled={
                                                item.item_status !== "ACTIVE" ||
                                                item.is_verified ||
                                                processingItemId === item.id ||
                                                order.order_status !== "VERIFICATION_IN_PROGRESS"
                                            }
                                        >
                                            Request Replacement
                                        </button>

                                        {replacementItemId === item.id && (
                                            <div className="action-panel replacement-panel">
                                                <h4>Request Replacement</h4>
                                                <p>
                                                    Select the reason for requesting a replacement.
                                                </p>

                                                <select
                                                    value={replacementReason}
                                                    onChange={(e) =>
                                                        setReplacementReason(e.target.value)
                                                    }
                                                >
                                                    <option value="">
                                                        Select replacement reason
                                                    </option>

                                                    {replacementReasons.map((reason) => (
                                                        <option
                                                            key={reason.value}
                                                            value={reason.value}
                                                        >
                                                            {reason.label}
                                                        </option>
                                                    ))}
                                                </select>

                                                <div className="panel-actions">
                                                    <button
                                                        className="close-panel-button"
                                                        onClick={() => {
                                                            setReplacementItemId(null);
                                                            setReplacementReason("");
                                                        }}
                                                    >
                                                        Cancel
                                                    </button>

                                                    <button
                                                        className="confirm-replacement-button"
                                                        onClick={handleConfirmReplacement}
                                                        disabled={
                                                            !replacementReason ||
                                                            isRequestingReplacement
                                                        }
                                                    >
                                                        {isRequestingReplacement
                                                            ? "Submitting..."
                                                            : "Confirm Replacement"}
                                                    </button>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </article>
                        );
                    })}
                </div>
            </section>

            <section className="verification-footer">
                {hasPendingReplacement && (
                    <div className="pending-replacement-message">
                        <span>!</span>
                        <p>Waiting for supervisor approval on replacement request.</p>
                    </div>
                )}

                <button
                    className="complete-verification-button"
                    onClick={handleCompleteVerification}
                    disabled={
                        hasPendingItems ||
                        hasPendingReplacement ||
                        processingItemId === "complete"
                    }
                >
                    {processingItemId === "complete"
                        ? "Completing..."
                        : "✓ Complete Verification"}
                </button>
            </section>
        </main>
    );
}

export default TakeawayOrderVerificationPage;
