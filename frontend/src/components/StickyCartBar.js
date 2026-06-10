import { Link } from "react-router-dom";
import { ShoppingBag, ChevronRight } from "lucide-react";
import { useApp } from "../context/AppContext";

export const StickyCartBar = () => {
  const { totals, discountInfo } = useApp();
  if (totals.itemCount === 0) return null;

  return (
    <Link
      to="/cart"
      className="fixed bottom-4 left-4 right-4 sm:left-1/2 sm:-translate-x-1/2 sm:w-[640px] sm:max-w-[calc(100%-2rem)] z-50 bg-teal-700 hover:bg-teal-800 transition-colors cart-shadow rounded-2xl px-4 py-3 flex items-center justify-between text-white fade-up"
      data-testid="cart-sticky-summary"
    >
      <div className="flex items-center gap-3">
        <div className="relative w-10 h-10 rounded-xl bg-teal-800 flex items-center justify-center">
          <ShoppingBag className="w-5 h-5 text-yellow-300" />
          <span
            className="absolute -top-1 -right-1 min-w-[20px] h-5 px-1 rounded-full bg-orange-500 text-white text-[11px] font-bold flex items-center justify-center"
            data-testid="cart-sticky-count"
          >
            {totals.itemCount}
          </span>
        </div>
        <div className="leading-tight">
          <div className="font-display font-bold text-base" data-testid="cart-sticky-total">
            ₹{totals.total.toFixed(0)}
          </div>
          {discountInfo.discount > 0 && (
            <div className="text-[11px] text-yellow-300/90 line-through">
              ₹{totals.subtotal.toFixed(0)}
            </div>
          )}
        </div>
      </div>
      <div className="flex items-center gap-1 font-semibold text-sm">
        View Cart <ChevronRight className="w-4 h-4" />
      </div>
    </Link>
  );
};
