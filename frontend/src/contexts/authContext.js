import { createContext } from "react";
import { useLocalStorage } from "../hooks/useLocalStorage";
import * as authService from "../services/authService";
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

    const userUpdate = async (formData, user_id) => {
        try {
            return await authService.update(formData, user_id);
        } catch (error) {
            throw error;
        }
    };

    const userLogout = () => {
        setAuth(null);
    };

    const userContextData = {
        user: auth?.user,
        token: auth?.token,
        userUpdate,
        userLogin,
        userLogout
    };

    return (
        <AuthContext.Provider value={userContextData}>
            {children}
        </AuthContext.Provider>
    );
};