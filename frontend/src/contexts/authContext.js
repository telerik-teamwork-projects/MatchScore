import { createContext, useEffect } from "react";
import { useLocalStorage } from "../hooks/useLocalStorage";
import * as authService from "../services/authService";

export const AuthContext = createContext("auth", null);

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useLocalStorage("auth", null);

    useEffect(() => {
        if (auth?.token) {
            const checkTokenExpiration = async () => {
                try {
                    const decodedToken = await authService.verifyToken(
                        auth.token
                    );
                    setAuth((prevAuth) => ({
                        ...prevAuth,
                        user: decodedToken,
                    }));
                } catch (error) {
                    console.error(error);
                    setAuth(null);
                }
            };
            checkTokenExpiration();
        }
    }, [auth?.token, setAuth]);

    const userLogin = async (userData) => {
        try {
            const user = await authService.login(userData);
            setAuth(user);
        } catch (error) {
            throw error;
        }
    };

    const userUpdate = async (formData, user_id, token) => {
        try {
            return await authService.update(formData, user_id, token);
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
        userLogout,
    };

    return (
        <AuthContext.Provider value={userContextData}>
            {children}
        </AuthContext.Provider>
    );
};
