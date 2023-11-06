import { Routes, Route } from "react-router-dom";

import { Home } from "./pages/home/Home";
import { Layout } from "./components/layout/Layout";
import { Login } from "./pages/login/Login";
import { Register } from "./pages/register/Register";
import { Profile } from "./pages/profile/Profile";

import { AuthProvider } from "./components/contexts/authContext";
import { HOME, LOGIN, PROFILE, REGISTER } from "./routes/routes";

function App() {
    return (
        <AuthProvider>
            <Layout>
                <Routes>
                    <Route path={HOME} element={<Home />} />
                    <Route path={LOGIN} element={<Login />} />
                    <Route path={REGISTER} element={<Register />} />
                    <Route path={PROFILE} element={<Profile />} />
                </Routes>
            </Layout>
        </AuthProvider>
    );
}

export default App;
