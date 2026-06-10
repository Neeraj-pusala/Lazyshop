import { Plus, Minus } from "lucide-react";
import { useApp } from "../context/AppContext";

export const ProductCard = ({ product }) => {
  const { addToCart, decrement, cart, discountInfo } = useApp();
  const inCart = cart.find((c) => c.product_id === product.id);
  const qty = inCart ? inCart.quantity : 0;
  const discounted = product.original_price * (1 - discountInfo.discount / 100);

  return (
    <div
      className="flex flex-col bg-white rounded-2xl p-3 sm:p-4 border border-gray-100 hover:shadow-md hover:border-teal-700/20 transition-all duration-300 group fade-up"
      data-testid={`product-card-${product.id}`}
    >
      <div className="relative aspect-square overflow-hidden rounded-xl bg-gray-50 mb-3">
        <img
          src={product.image}
          alt={product.name}
          loading="lazy"
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          onError={(e) => {
            e.currentTarget.src =
              "https://images.unsplash.com/photo-1481349518771-20055b2a7b24?w=600&q=80";
          }}
        />
        {discountInfo.discount > 0 && (
          <span className="absolute top-2 left-2 bg-orange-500 text-white text-[10px] font-bold px-2 py-1 rounded-full">
            {discountInfo.discount}% OFF
          </span>
        )}
      </div>

      <h3
        className="font-display font-semibold text-sm sm:text-base text-gray-900 leading-snug line-clamp-2 min-h-[2.6rem]"
        data-testid={`product-name-${product.id}`}
      >
        {product.name}
      </h3>
      <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">{product.description}</p>

      <div className="mt-3 flex items-end justify-between gap-2">
        <div className="leading-tight">
          <div
            className="font-display font-bold text-base sm:text-lg text-teal-700"
            data-testid={`product-discounted-price-${product.id}`}
          >
            ₹{discounted.toFixed(0)}
          </div>
          {discountInfo.discount > 0 && (
            <div
              className="text-xs text-gray-400 line-through"
              data-testid={`product-original-price-${product.id}`}
            >
              ₹{product.original_price}
            </div>
          )}
        </div>

        {qty === 0 ? (
          <button
            onClick={() => addToCart(product)}
            className="bg-yellow-300 text-gray-900 font-semibold rounded-lg px-3 py-2 hover:bg-yellow-400 active:scale-95 transition-all text-xs sm:text-sm shadow-sm inline-flex items-center gap-1"
            data-testid={`add-to-cart-button-${product.id}`}
          >
            <Plus className="w-3.5 h-3.5" />
            ADD
          </button>
        ) : (
          <div
            className="inline-flex items-center bg-teal-700 text-white rounded-lg overflow-hidden"
            data-testid={`qty-controls-${product.id}`}
          >
            <button
              onClick={() => decrement(product.id)}
              className="px-2 py-2 hover:bg-teal-800 active:scale-95 transition-all"
              data-testid={`decrement-button-${product.id}`}
              aria-label="Decrease quantity"
            >
              <Minus className="w-3.5 h-3.5" />
            </button>
            <span className="px-2 text-sm font-bold min-w-[20px] text-center" data-testid={`qty-${product.id}`}>
              {qty}
            </span>
            <button
              onClick={() => addToCart(product)}
              className="px-2 py-2 hover:bg-teal-800 active:scale-95 transition-all"
              data-testid={`increment-button-${product.id}`}
              aria-label="Increase quantity"
            >
              <Plus className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
