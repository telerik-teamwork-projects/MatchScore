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

export const login = async (userData) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/users/login`,
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

export const getUser = async (userId, token) => {
    try {
        const response = await axios.get(
            `${USER_BASE_PATH}/users/${userId}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getUsers = async (searchQ) => {
    try {
        const response = await axios.get(`${USER_BASE_PATH}/users/`, {
            params: searchQ,
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};
