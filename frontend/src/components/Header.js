import { Link, useNavigate } from "react-router-dom";
import { ShoppingBag, LogOut, Package, Sparkles } from "lucide-react";
import { useApp } from "../context/AppContext";

export const Header = () => {
  const { studentId, discountInfo, totals, logout } = useApp();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <header className="sticky top-0 z-40 bg-white/85 backdrop-blur-xl border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <Link to="/shop" className="flex items-center gap-2" data-testid="header-logo">
          <div className="w-9 h-9 rounded-xl bg-teal-700 flex items-center justify-center">
            <ShoppingBag className="w-5 h-5 text-yellow-300" strokeWidth={2.5} />
          </div>
          <div className="leading-tight">
            <div className="font-display font-bold text-lg tracking-tight text-gray-900">Lazy Shop</div>
            <div className="text-[10px] text-gray-500 -mt-0.5">For College, By Lazy</div>
          </div>
        </Link>

        <div className="flex items-center gap-2 sm:gap-3">
          {studentId && (
            <div
              className="hidden sm:flex items-center gap-2 bg-yellow-300/40 border border-yellow-300 rounded-full pl-3 pr-4 py-1.5"
              data-testid="header-discount-badge"
            >
              <Sparkles className="w-4 h-4 text-orange-500" />
              <span className="text-xs font-semibold text-gray-900">
                {discountInfo.year} · {discountInfo.discount}% OFF
              </span>
            </div>
          )}

          <Link
            to="/orders"
            className="hidden sm:inline-flex items-center gap-1.5 text-sm font-medium text-gray-700 hover:text-teal-700 px-3 py-2 rounded-lg transition-colors"
            data-testid="header-orders-link"
          >
            <Package className="w-4 h-4" />
            Orders
          </Link>

          <Link
            to="/cart"
            className="relative inline-flex items-center justify-center w-10 h-10 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors"
            data-testid="header-cart-icon"
          >
            <ShoppingBag className="w-5 h-5 text-gray-900" />
            {totals.itemCount > 0 && (
              <span
                className="absolute -top-1 -right-1 min-w-[20px] h-5 px-1 rounded-full bg-orange-500 text-white text-[11px] font-bold flex items-center justify-center pop-in"
                data-testid="header-cart-badge"
              >
                {totals.itemCount}
              </span>
            )}
          </Link>

          <button
            onClick={handleLogout}
            className="inline-flex items-center justify-center w-10 h-10 rounded-full hover:bg-gray-100 transition-colors"
            data-testid="header-logout-button"
            aria-label="Logout"
          >
            <LogOut className="w-4 h-4 text-gray-600" />
          </button>
        </div>
      </div>
    </header>
  );
};
