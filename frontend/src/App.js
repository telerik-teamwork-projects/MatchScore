import { Routes, Route } from "react-router-dom";

import { Home } from "./pages/home/Home";
import { Layout } from "./components/layout/Layout";
import { Login } from "./pages/login/Login";
import { Register } from "./pages/register/Register";
import { Profile } from "./pages/profile/Profile";

import { AuthProvider } from "./components/contexts/authContext";
import { HOME, LOGIN, PROFILE, REGISTER } from "./routes/routes";
import { AuthRouteGuard } from "./routeGuards/authRouteGuard";
import { NoAuthRouteGuard } from "./routeGuards/noAuthRouteGuard";

function App() {
    return (
        <AuthProvider>
            <Layout>
                <Routes>
                    <Route element={<NoAuthRouteGuard />}>
                        <Route path={LOGIN} element={<Login />} />
                        <Route path={REGISTER} element={<Register />} />
                    </Route>

                    <Route path={HOME} element={<Home />} />
                    <Route element={<AuthRouteGuard />}>
                        <Route path={PROFILE} element={<Profile />} />
                    </Route>
                </Routes>
            </Layout>
        </AuthProvider>
    );
}

export default App;
