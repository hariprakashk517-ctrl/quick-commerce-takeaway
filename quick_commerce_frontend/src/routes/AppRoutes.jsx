import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "../pages/auth/LoginPage";
import CustomerDashboard from "../pages/customer/CustomerDashboard";
import PackerDashboard from "../pages/packer/PackerDashboard";
import AdminDashboard from "../pages/admin/AdminDashboard";
import SupervisorDashboard from "../pages/supervisor/SupervisorDashboard";
import TakeawayDashboard from "../pages/takeaway/TakeawayDashboard";
import UnauthorizedPage from "../pages/common/UnauthorizedPage";
import ProtectedRoute from "./ProtectedRoute";
import RoleRoute from "./RoleRoute";
import AddressListPage from "../pages/customer/address/AddressListPage";
import AddAddressPage from "../pages/customer/address/AddAddressPage";
import EditAddressPage from "../pages/customer/address/EditAddressPage";
import ProductListPage from "../pages/customer/product/ProductListPage";
import ProductDetailPage from "../pages/customer/product/ProductDetailPage";
import CartPage from "../pages/customer/cart/CartPage";
import CheckoutPage from "../pages/customer/checkout/CheckoutPage";
import OrderSuccessPage from "../pages/customer/orders/OrderSuccessPage";
import CustomerOrdersPage from "../pages/customer/orders/CustomerOrdersPage";
import CustomerOrderDetailPage from "../pages/customer/orders/CustomerOrderDetailPage";
import PickupCredentialsPage from "../pages/customer/orders/PickupCredentialsPage";
import PackingQueuePage from "../pages/packer/PackingQueuePage";
import PackingDetailsPage from "../pages/packer/PackingDetailsPage";
import BoxAssignmentQueuePage from "../pages/takeaway/BoxAssignmentQueuePage";
import AssignBoxPage from "../pages/takeaway/AssignBoxPage";
import BoxAssignedOrdersPage from "../pages/takeaway/BoxAssignedOrdersPage";
import TakeawayQRScannerPage from "../pages/takeaway/TakeawayQRScannerPage";
import TakeawayOrderVerificationPage from "../pages/takeaway/TakeawayOrderVerificationPage";
import ReplacementRequestsPage from "../pages/supervisor/ReplacementRequestsPage";
import ReplacementRequestDetailPage from "../pages/supervisor/ReplacementRequestDetailPage";
import ProfilePage from "../pages/profile/ProfilePage";
import PaymentSummaryPage from "../pages/takeaway/PaymentSummaryPage";
import VerifyPickupOTPPage from "../pages/takeaway/VerifyPickupOTPPage";
import CompletePickupPage from "../pages/takeaway/CompletePickupPage";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />

        <Route
          path="/customer"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["CUSTOMER"]}>
                <CustomerDashboard />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/customer/addresses"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["CUSTOMER"]}>
                <AddressListPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/customer/addresses/add"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["CUSTOMER"]}>
                <AddAddressPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/customer/addresses/:addressId/edit"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["CUSTOMER"]}>
                <EditAddressPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/customer/products"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["CUSTOMER"]}>
                <ProductListPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/customer/products/:productId"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["CUSTOMER"]}>
                <ProductDetailPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/customer/cart"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["CUSTOMER"]}>
                <CartPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/customer/checkout"
          element={<CheckoutPage />}
        />

        <Route
          path="/customer/orders/:orderId/success"
          element={
            <RoleRoute allowedRoles={["CUSTOMER"]}>
              <OrderSuccessPage />
            </RoleRoute>
          }
        />

        <Route
          path="/customer/orders"
          element={
            <RoleRoute allowedRoles={["CUSTOMER"]}>
              <CustomerOrdersPage />
            </RoleRoute>
          }
        />

        <Route
          path="/customer/orders/:orderId"
          element={
            <RoleRoute allowedRoles={["CUSTOMER"]}>
              <CustomerOrderDetailPage />
            </RoleRoute>
          }
        />

        <Route
          path="/customer/orders/:orderId/pickup-credentials"
          element={
            <RoleRoute allowedRoles={["CUSTOMER"]}>
              <PickupCredentialsPage />
            </RoleRoute>
          }
        />

        <Route
          path="/profile"
          element={
            <RoleRoute allowedRoles={["CUSTOMER"]}>
              <ProfilePage />
            </RoleRoute>
          }
        />

        <Route
          path="/packer"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["PACKER"]}>
                <PackerDashboard />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

          <Route 
            path="/packer/packing"
            element={
              <ProtectedRoute>
                <RoleRoute allowedRoles={["PACKER"]}>
                  <PackingQueuePage />
                </RoleRoute>
              </ProtectedRoute>
            }
          />

          <Route
            path="/packer/packing/:orderId"
            element={
              <ProtectedRoute>
                  <RoleRoute allowedRoles={["PACKER"]}>
                      <PackingDetailsPage />
                  </RoleRoute>
              </ProtectedRoute>
            }
          />  

        <Route
          path="/takeaway"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["TAKEAWAY_STAFF"]}>
                <TakeawayDashboard />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/takeaway/box-assign"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["TAKEAWAY_STAFF"]}>
                <BoxAssignmentQueuePage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/takeaway/box-assign/:orderId"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["TAKEAWAY_STAFF"]}>
                <AssignBoxPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route 
          path="/takeaway/box-assigned/"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["TAKEAWAY_STAFF"]}>
                <BoxAssignedOrdersPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/takeaway/scan-qr"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["TAKEAWAY_STAFF","ADMIN","SUPERVISOR",]}>
                <TakeawayQRScannerPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/takeaway/order-verification/:orderId"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["TAKEAWAY_STAFF"]}>
                <TakeawayOrderVerificationPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/takeaway/payment-summary/:orderId"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["TAKEAWAY_STAFF"]}>
                <PaymentSummaryPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/takeaway/verify-otp/:orderId"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["TAKEAWAY_STAFF"]}>
                <VerifyPickupOTPPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/takeaway/complete-pickup/:orderId"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["TAKEAWAY_STAFF"]}>
                <CompletePickupPage />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/supervisor"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["SUPERVISOR"]}>
                <SupervisorDashboard />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/supervisor/replacement-requests"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["SUPERVISOR"]}>
                <ReplacementRequestsPage />
              </RoleRoute>
            </ProtectedRoute>
          }
       />

       <Route
          path="/supervisor/replacement-requests/:replacementRequestId"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["SUPERVISOR"]}>
                <ReplacementRequestDetailPage />
              </RoleRoute>
            </ProtectedRoute>
          }
      />

        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <RoleRoute allowedRoles={["ADMIN"]}>
                <AdminDashboard />
              </RoleRoute>
            </ProtectedRoute>
          }
        />

        <Route
          path="/unauthorized"
          element={
            <ProtectedRoute>
              <UnauthorizedPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;