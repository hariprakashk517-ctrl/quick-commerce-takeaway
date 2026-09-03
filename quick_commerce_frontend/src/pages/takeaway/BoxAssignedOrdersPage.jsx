import { useEffect, useState } from "react";
import { boxAssignedOrders } from "../../services/takeawayService";
import { markOutForPickup } from "../../services/orderService";

function BoxAssignedOrdersPage() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {fetchAssignedOrders()}, []);

    const fetchAssignedOrders = async () => {
        try {
            const response = await boxAssignedOrders();
            // console.log(response.data);

            setOrders(response.data.data);
        } catch (error) {
            setError(error.response?.data || error.message);
        } finally {
            setLoading(false);
        }
    }

    async function handleOutForPickup(orderId) {
        try{
            const response = await markOutForPickup(orderId)
            alert("Order moved out for pickup successfully")
            fetchAssignedOrders()
        } catch (error){
            setError(error.response?.data || error.message)
        }
    }

    if (loading) {return <h3>Loading...</h3>;}

    if (error) return <h2>{error}</h2>;

    return (
        <div>
            <h2>Box Assigned Orders</h2>

            {orders.length === 0 ? (
                <p>No assigned orders found</p>
            ) : (
                <table border="1">
                    <thead>
                        <tr>
                            <th>Order ID</th>
                            <th>Box ID</th>
                            <th>Status</th>
                            <th>Mark For Pickup</th>
                        </tr>
                    </thead>

                    <tbody>
                        {orders.map((order) => (
                            <tr key={order.id}>
                                <td>{order.order_id}</td>
                                <td>{order.box_id}</td>
                                <td>{order.order_status}</td>
                                <td>
                                    <button onClick={()=> handleOutForPickup(order.order_id)}disabled={loading}>
                                    {loading ? "Processing..." : "Out For Pickup"}
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default BoxAssignedOrdersPage;