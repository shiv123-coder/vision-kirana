import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { LandingPage } from "@/pages/LandingPage";
import { ShopRegistrationForm } from "@/features/shop/ShopRegistrationForm";
import { ShopEditForm } from "@/features/shop/ShopEditForm";
import { DashboardPage } from "@/pages/DashboardPage";
import { DocumentUploadView } from "@/features/application/DocumentUploadView";
import { ApplicationReportView } from "@/features/application/ApplicationReportView";
import { Navbar } from "@/components/layout/Navbar";
import SystemStatusPage from "@/pages/SystemStatusPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage />,
  },
  {
    path: "/register-shop",
    element: (
      <div className="min-h-screen bg-background">
        <Navbar />
        <ShopRegistrationForm />
      </div>
    ),
  },
  {
    path: "/dashboard",
    element: <DashboardPage />,
  },
  {
    path: "/shops/:shopId/edit",
    element: (
      <div className="min-h-screen bg-background">
        <Navbar />
        <ShopEditForm />
      </div>
    ),
  },
  {
    path: "/applications/:applicationId/documents",
    element: (
      <div className="min-h-screen bg-background">
        <Navbar />
        <DocumentUploadView />
      </div>
    ),
  },
  {
    path: "/applications/:applicationId/report",
    element: <ApplicationReportView />,
  },
  {
    path: "/system-status",
    element: (
      <div className="min-h-screen bg-background">
        <Navbar />
        <SystemStatusPage />
      </div>
    ),
  }
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}

