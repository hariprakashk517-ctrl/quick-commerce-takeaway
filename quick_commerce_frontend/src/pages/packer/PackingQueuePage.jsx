import { useState, useEffect } from "react";
import { getPackingOrders,startPacking } from "../../services/packingService";
import { useNavigate } from "react-router-dom";

function PackingQueuePage() {
    const [packingOrders, setPackingOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    useEffect(()=>{
        fetchPackingOrders();
    }, []);

    async function fetchPackingOrders() {
        try {
            setLoading(true);
            setError("");
            const response = await getPackingOrders();
            setPackingOrders(response.data.data)
        } catch (error){
            const errorMessage = error.response?.data?.message || "Unable to load packing orders.";
            setError(errorMessage);
        } finally{
            setLoading(false)
        }
    }

    async function handleStartPacking(orderId) {
    try {
        const response = await startPacking(orderId);

        navigate(`/packer/packing/${orderId}`);
    } catch (err) {
        const errorMessage = err.response?.data?.message|| "Unable to start packing."
        setError(errorMessage)
    }
}

    if (loading) {
        return <h2>Loading packing queue...</h2>;
    }

    if (error) {
        return <h2>{error}</h2>;
    }

    if (packingOrders.length === 0) {
        return <h2>No orders waiting for packing.</h2>;
    }
    return (
       <div className="packing-queue">
            {packingOrders.map((order) => (
                <div key={order.id} className="packing-order-card">
                    <p>
                        <strong>Order ID:</strong> {order.order_id || "N/A"}
                    </p>

                    <p>
                        <strong>Store:</strong> {order.store_name}
                    </p>

                    <p>
                        <strong>Fulfillment:</strong> {order.fulfillment_mode}
                    </p>

                    <p>
                        <strong>Status:</strong> {order.order_status}
                    </p>

                    {/* <p>
                        <strong>Payment:</strong> {order.payment_status}
                    </p> */}

                    {/* <p>
                        <strong>Total:</strong> ₹{order.total_amount}
                    </p> */}

                    {/* <strong>Items:</strong>
                    <ul>
                        {order.items?.map((item) => (
                            <li key={item.id}>
                                {item.product_name} × {item.quantity}
                            </li>
                        ))}
                    </ul> */}

                    {/* <p>
                        <strong>Created:</strong>{" "}
                        {new Date(order.created_at).toLocaleString()}
                    </p> */}

                    <button onClick={() => handleStartPacking(order.order_id)}>Start Packing</button>
                </div>
            ))}
        </div>
    );
}

export default PackingQueuePage;
