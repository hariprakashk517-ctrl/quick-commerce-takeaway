import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { assignBox } from "../../services/takeawayService";

function AssignBoxPage() {
    const { orderId } = useParams();
    const navigate = useNavigate();
    const [boxId, setBoxId] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    async function handleSubmit(e) {
        e.preventDefault();
        try {
            setError("");
            const response = await assignBox({order_id: orderId,box_id: boxId,});
            alert("Box assigned successfully");
            setMessage(response.data.message);
            navigate("/takeaway/box-assign");
        } catch (err) {
            setMessage("");
            setError(err.response?.data?.message || "Unable to assign box.");
            // console.log("API Error:", error.response?.data);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Order ID</label>
                <input value={orderId}readOnly />
            </div> 
            <div>
                <label>Box ID</label>
                <input value={boxId} onChange={(e) =>setBoxId(e.target.value)} placeholder="Enter Box ID" required/>
            </div>
            <button type="submit">
                Assign Box
            </button>
            {message && (<p style={{ color: "green" }}>{message}</p>)}
            {error && (<p style={{ color: "red" }}>{error}</p>)}
        </form>
    );
}

export default AssignBoxPage;