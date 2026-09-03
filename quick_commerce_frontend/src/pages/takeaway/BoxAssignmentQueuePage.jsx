import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPackingDoneOrders } from "../../services/takeawayService";

function BoxAssignmentQueuePage() {
    const navigate = useNavigate();

    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {fetchOrders();}, []);

    async function fetchOrders() {
        try {
            setLoading(true);
            setError("");

            const response = await getPackingDoneOrders();
            // console.log(response.data);
            setOrders(response.data.data);
        } catch (err) {
            setError(err.response?.data?.message || "Unable to load orders.");
        } finally {
            setLoading(false);
        }
    }

    if (loading) return <h2>Loading...</h2>;

    if (error) return <h2>{error}</h2>;

    if (orders.length === 0) {
        return <h2>No packing completed orders.</h2>;
    }

    return (
        <div className="box-assignment-queue">
            {orders.map((order) => (
                <div key={order.id} className="box-order-card">
                    <p>
                        <strong>Order ID:</strong>{" "}
                        {order.order_id}
                    </p>
                    <p>
                        <strong>Store:</strong>{" "}
                        {order.store_name}
                    </p>
                    <p>
                        <strong>Status:</strong>{" "}
                        {order.order_status}
                    </p>
                    <button onClick={() => navigate(`/takeaway/box-assign/${order.order_id}`)}>
                    Assign Box
                    </button>
                </div>
            ))}
        </div>
    );
}

export default BoxAssignmentQueuePage;