import { Route, Routes, useLocation, useNavigate } from "react-router-dom"
// pages imports
import ProtectedRoutes from "@/lib/protected-routes"
import Placeholder from "@/pages/Placeholder"
import Login from "@/pages/access/Login"
import Register from "@/pages/access/Register"
import Home from "@/pages/Home"
import PageNotFound from "@/pages/PageNotFound"
import DynamicsPage from "@/pages/dynamics/Dynamics"
import FdsDataPage from "@/pages/fds-data/FdsData"
import { useAuth } from "@/contexts/AuthProvider"
import { useEffect } from "react"
import { ThemeProvider } from "@/components/theme-provider"
import { Toaster } from "@/components/ui/sonner";

const App: React.FC = () => {
  const navigate = useNavigate()
  const { auth } = useAuth()
  const { pathname } = useLocation()

  useEffect(() => {
    if (auth?.token && (pathname === "/login" || pathname === "/register")) {
      navigate("/")
    }
  }, [auth, pathname])

  return (
    <ThemeProvider defaultTheme="light" storageKey="dma-ui-theme">
      <Toaster />
      <Routes>
        <Route path="/" element={<ProtectedRoutes />}>
          {/* Home as a layout for nested routes */}
          <Route path="/" element={<Home />}>
            <Route index element={<div>Welcome to Home</div>} /> {/* Default content */}
            <Route path="dynamics" element={<DynamicsPage />} /> {/* Nested DynamicsPage */}
            <Route path="fds-data" element={<FdsDataPage />} /> {/* Nested DynamicsPage */}
          </Route>
        </Route>

        <Route path="/landing" element={<Placeholder />} />
        <Route path="/terms" element={<Placeholder />} />
        <Route path="/privacy" element={<Placeholder />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>

    </ThemeProvider>




  )
}

export default App
