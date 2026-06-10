import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "sonner";
import { AppProvider, useApp } from "@/context/AppContext";
import Login from "@/pages/Login";
import Catalog from "@/pages/Catalog";
import Cart from "@/pages/Cart";
import Orders from "@/pages/Orders";

const Protected = ({ children }) => {
  const { studentId } = useApp();
  if (!studentId) return <Navigate to="/" replace />;
  return children;
};

const PublicOnly = ({ children }) => {
  const { studentId } = useApp();
  if (studentId) return <Navigate to="/shop" replace />;
  return children;
};

function App() {
  return (
    <div className="App">
      <AppProvider>
        <BrowserRouter>
          <Toaster position="top-center" richColors />
          <Routes>
            <Route
              path="/"
              element={
                <PublicOnly>
                  <Login />
                </PublicOnly>
              }
            />
            <Route
              path="/shop"
              element={
                <Protected>
                  <Catalog />
                </Protected>
              }
            />
            <Route
              path="/cart"
              element={
                <Protected>
                  <Cart />
                </Protected>
              }
            />
            <Route
              path="/orders"
              element={
                <Protected>
                  <Orders />
                </Protected>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AppProvider>
    </div>
  );
}

export default App;
