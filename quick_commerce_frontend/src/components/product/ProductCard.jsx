import { useEffect,useState } from "react";
import { useNavigate } from "react-router-dom";
import { addCartItem, updateCartItem, removeCartItem } from "../../services/cartService";
import "./ProductCard.css";

function ProductCard({ product, cartQuantity = 0, onCartUpdate }) {
    const navigate = useNavigate();
    const [quantity, setQuantity] = useState(cartQuantity);
    const [isUpdating, setIsUpdating] = useState(false);

    useEffect(() => {
        setQuantity(cartQuantity);
    }, [cartQuantity]);

    function handleViewProduct() {
        navigate(`/customer/products/${product.product_id}`);
    }

    async function handleAddToCart(event) {
        event.stopPropagation();

        try {
            setIsUpdating(true);
            await addCartItem(product.product_id, 1);
            setQuantity(1);

            if (onCartUpdate) {
                await onCartUpdate();
            }
        } catch (error) {
            alert(
                error.response?.data?.message || "Unable to add product to cart.");
        } finally {
            setIsUpdating(false);
        }
    }

    async function handleIncrease(event) {
        event.stopPropagation();

        try {
            setIsUpdating(true);
            const newQuantity = quantity + 1;
            await updateCartItem(product.product_id,newQuantity);
            setQuantity(newQuantity);

            if (onCartUpdate) {
                await onCartUpdate();
            }
        } catch (error) {
            alert(
                error.response?.data?.message ||
                "Unable to update quantity."
            );
        } finally {
            setIsUpdating(false);
        }
    }

    async function handleDecrease(event) {
        event.stopPropagation();

        try {
            setIsUpdating(true);
            if (quantity === 1) {
                await removeCartItem(product.product_id);
                setQuantity(0);
            } else {
                const newQuantity = quantity - 1;
                await updateCartItem(product.product_id,newQuantity);

                setQuantity(newQuantity);
            }

            if (onCartUpdate) {
                onCartUpdate();
            }
        } catch (error) {
            alert(
                error.response?.data?.message || "Unable to update cart.");
        } finally {
            setIsUpdating(false);
        }
    }

    return (
        <article
            className="product-card"
            onClick={handleViewProduct}>
            <div className="product-image-box">
                {product.image_url ? (
                    <img src={product.image_url} alt={product.product_name}/>
                ) : (
                    <span className="product-image-placeholder">
                        🛒
                    </span>
                )}
            </div>

            <div className="product-card-content">
                <h3 className="product-name">
                    {product.product_name}
                </h3>

                <p className="product-description">
                    {product.description || "No description available."}
                </p>

                <div className="product-card-bottom">
                    <p className="product-price">
                        ₹{product.price}
                    </p>

                    {!product.can_add_to_cart ? (
                        <button type="button" className="product-cart-button unavailable" disabled onClick={(event) => event.stopPropagation()}>
                            Unavailable
                        </button>
                    ) : quantity === 0 ? (
                        <button type="button" className="product-cart-button" disabled={isUpdating} onClick={handleAddToCart}>
                            {isUpdating ? "..." : "ADD"}
                        </button>
                    ) : (
                        <div className="product-quantity-control"
                            onClick={(event) => event.stopPropagation()}>
                            <button type="button" className="product-quantity-button" disabled={isUpdating} onClick={handleDecrease}>
                                −
                            </button>

                            <span className="product-quantity-value">
                                {quantity}
                            </span>

                            <button type="button" className="product-quantity-button" disabled={isUpdating} onClick={handleIncrease}>
                                +
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </article>
    );
}

export default ProductCard;