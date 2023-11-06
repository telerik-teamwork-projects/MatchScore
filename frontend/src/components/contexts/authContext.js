import { createContext } from "react";
import { useLocalStorage } from "../hooks/useLocalStorage";
import * as authService from "../../services/authService";

export const AuthContext = createContext("auth", null);

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useLocalStorage("auth", null);

    const userLogin = async (userData) => {
        try {
            const user = await authService.login(userData);
            setAuth(user);
        } catch (error) {
            throw error;
        }
    };

    const userContextData = {
        user: auth?.user,
        token: auth?.token,
        userLogin,
    };

    return (
        <AuthContext.Provider value={userContextData}>
            {children}
        </AuthContext.Provider>
    );
};
