import { useContext } from "react";

import { AuthContext } from "../contexts/authContext";
import { Navigate, Outlet } from "react-router-dom";
import { LOGIN } from "../routes/routes";

export const AuthRouteGuard = ({ children }) => {
    const { token } = useContext(AuthContext);
    if (!token) {
        return <Navigate to={LOGIN} />;
    }

    return children ? children : <Outlet />;
};
