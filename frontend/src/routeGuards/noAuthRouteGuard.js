import { useContext } from "react";

import { AuthContext } from "../contexts/authContext";
import { Navigate, Outlet } from "react-router-dom";
import { HOME } from "../routes/routes";

export const NoAuthRouteGuard = ({ children }) => {
    const { token } = useContext(AuthContext);
    if (token) {
        return <Navigate to={HOME} />;
    }

    return children ? children : <Outlet />;
};
