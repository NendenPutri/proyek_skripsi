import { Route, Routes } from "react-router-dom";
import { AdminLayout, MainLayout, ProtectedRoute } from "./components/layouts";
import AuthProvider from "./contexts/AuthProvider";
import AdminDashboardPage from "./pages/AdminDashboardPage";
import AdminLaptopCreatePage from "./pages/AdminLaptopCreatePage";
import AdminLaptopDetailPage from "./pages/AdminLaptopDetailPage";
import AdminLaptopEditPage from "./pages/AdminLaptopEditPage";
import AdminLaptopsPage from "./pages/AdminLaptopsPage";
import AdminLoginPage from "./pages/AdminLoginPage";
import AboutPage from "./pages/AboutPage";
import HomePage from "./pages/HomePage";
import LaptopsPage from "./pages/LaptopsPage";
import NotFoundPage from "./pages/NotFoundPage";
import RecommendationPage from "./pages/RecommendationPage";
import AOS from "aos";
import "aos/dist/aos.css";
import { useEffect } from "react";

function App() {
  useEffect(() => {
    AOS.init({
      once: true,
      delay: 500,
      offset: 100,
    });
  });
  return (
    <AuthProvider>
      <Routes>
        <Route path="admin/login" element={<AdminLoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="admin" element={<AdminLayout />}>
            <Route index element={<AdminDashboardPage />} />
            <Route path="laptops" element={<AdminLaptopsPage />} />
            <Route path="laptops/create" element={<AdminLaptopCreatePage />} />
            <Route path="laptops/:id" element={<AdminLaptopDetailPage />} />
            <Route path="laptops/:id/edit" element={<AdminLaptopEditPage />} />
          </Route>
        </Route>
        <Route element={<MainLayout />}>
          <Route index element={<HomePage />} />
          <Route path="recommendation" element={<RecommendationPage />} />
          <Route path="laptops" element={<LaptopsPage />} />
          <Route path="about" element={<AboutPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}

export default App;
