import { Routes, Route } from "react-router-dom";

import { Home } from "./pages/Home";
import { Layout } from "./components/layout/Layout";
import { Login } from "./pages/login/Login";
import { Register } from "./pages/register/Register";

function App() {
    return (
        <Layout>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
            </Routes>
        </Layout>
    );
}

export default App;
