import axios from "axios";

import { BASE_PATH } from "../routes/paths";

export const register = async (userData) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/users/`,
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
            `${BASE_PATH}/users/login/`,
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

export const verifyToken = async (token) => {
    try {
        const response = await axios.get(`${BASE_PATH}/users/verify-token/`, {
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const update = async (formData, userId, token) => {
    try {
        const formDataToSend = new FormData();
        formDataToSend.append("username", formData.username);
        formDataToSend.append("email", formData.email);
        formDataToSend.append("bio", formData.bio);
        formDataToSend.append("profile_img", formData.profile_img);
        formDataToSend.append("cover_img", formData.cover_img);

        const response = await axios.put(
            `${BASE_PATH}/users/${userId}/`,
            formDataToSend,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const deleteUser = async (userId) => {
    try {
        const response = await axios.delete(`${BASE_PATH}/users/${userId}/`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getUser = async (userId, token) => {
    try {
        const response = await axios.get(
            `${BASE_PATH}/users/${userId}/`,
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
