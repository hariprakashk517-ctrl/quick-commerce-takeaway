import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {getPackingOrderById,completePacking,} from "../../services/packingService";

function PackingDetailsPage() {
    const { orderId } = useParams();
    const navigate = useNavigate();
    const [order, setOrder] = useState(null);
    const [checkedItems, setCheckedItems] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {fetchOrder();}, []);

    async function fetchOrder() {
        try {
            setLoading(true);
            const response = await getPackingOrderById(orderId);
            const orderData = response.data.data;
            setOrder(orderData);
            const checks = {};
            orderData.items.forEach((item) => {
                checks[item.id] = false;
            });
            setCheckedItems(checks);
        } catch (error) {
            setError(error.response?.data?.message || "Unable to load order.");
        } finally {
            setLoading(false);
        }
    }

    function toggleItem(itemId) {
        setCheckedItems((prev) => ({
            ...prev,
            [itemId]: !prev[itemId],
        }));
    }

    const allChecked = order && order.items.every((item) => checkedItems[item.id]);

    async function handleCompletePacking() {
        try {
            await completePacking(order.order_id);

            alert("Packing completed successfully.");

            navigate("/packer/packing");
        } catch (error) {
            alert(
                error.response?.data?.message ||
                    "Unable to complete packing."
            );
        }
    }

    if (loading) return <h2>Loading...</h2>;

    if (error) return <h2>{error}</h2>;

    return (
        <div className="packing-details">
            <h2>Packing Order</h2>

            <p>
                <strong>Order ID:</strong> {order.order_id}
            </p>

            <p>
                <strong>Store:</strong> {order.store_name}
            </p>

            <p>
                <strong>Fulfillment:</strong> {order.fulfillment_mode}
            </p>

            <hr />

            <h3>Items</h3>

            {order.items.map((item) => (
                <div
                    key={item.id}
                    className="packing-item"
                >
                    <input
                        type="checkbox"
                        checked={checkedItems[item.id]}
                        onChange={() =>
                            toggleItem(item.id)
                        }
                    />

                    <span>
                        {item.product_name}
                    </span>

                    <span>
                        Qty : {item.quantity}
                    </span>
                </div>
            ))}

            <br />

            <button disabled={!allChecked} onClick={handleCompletePacking}>
            Complete Packing
            </button>
        </div>
    );
}

export default PackingDetailsPage;