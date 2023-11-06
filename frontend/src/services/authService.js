import axios from "axios";

import { USER_BASE_PATH } from "../routes/paths";

export const register = async (userData) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/users/`,
            JSON.stringify(userData),
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const login = async ({ userData }) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/login`,
            JSON.stringify(userData),
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};
