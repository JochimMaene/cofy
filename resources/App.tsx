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
import SatellitesPage from "@/pages/satellite/Satellites"
import { useAuth } from "@/contexts/AuthProvider"
import { useEffect } from "react"
import { ThemeProvider } from "@/components/theme-provider"
import { Toaster } from "@/components/ui/sonner";
import MainLayout from "@/layouts/MainLayout"
import { MainNav } from "@/components/main-nav"
import { UserNav } from "@/components/user-nav"
import { Outlet } from "react-router-dom"
import GroundStationPage from "@/pages/ground-station/GroundStation"
import OrbitPage from "@/pages/orbit/Orbit"
import UtilPage from "@/pages/utilities/Utilities"

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
          <Route element={<MainLayout>
            <div className="hidden flex-col md:flex">
              <div className="border-b">
                <div className="flex h-16 items-center px-4">
                  <MainNav className="mx-6" />
                  <div className="ml-auto flex items-center space-x-4">
                    <UserNav />
                  </div>
                </div>
              </div>
            </div>
            <div className="p-4">
              <Outlet />
            </div>
          </MainLayout>}>
            <Route index element={<Home />} />
            <Route path="dynamics" element={<DynamicsPage />} />
            <Route path="fds-data" element={<FdsDataPage />} />
            <Route path="satellites" element={<SatellitesPage />} />
            <Route path="ground-stations" element={<GroundStationPage />} />
            <Route path="orbits" element={<OrbitPage />} />
            <Route path="utils" element={<UtilPage />} />
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
