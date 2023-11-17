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

export const update = async (formData, userId, token) => {
    try {
        const formDataToSend = new FormData();
        formDataToSend.append("username", formData.username);
        formDataToSend.append("email", formData.email);
        formDataToSend.append("bio", formData.bio);
        formDataToSend.append("profile_img", formData.profile_img);
        formDataToSend.append("cover_img", formData.cover_img);

        const response = await axios.put(
            `${USER_BASE_PATH}/users/${userId}/`,
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
        const response = await axios.delete(
            `${USER_BASE_PATH}/users/${userId}`
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
        const response = await axios.get(`${USER_BASE_PATH}/users`, {
            params: searchQ,
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const sendJoinTournamentRequestNoPlayer = async (
    tournamentId,
    token,
    playerData
) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/players/tournament-requests/${tournamentId}`,
            JSON.stringify(playerData),
            {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const sendJoinTournamentRequestWithPlayer = async (
    tournamentId,
    token,
    playerData
) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/players/tournament-requests/${tournamentId}/existing`,
            JSON.stringify(playerData),
            {
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const sendDirectorRequest = async (userId, userEmail, token) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/users/director-requests/`,
            { userId, userEmail },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getDirectorRequests = async (token) => {
    try {
        const response = await axios.get(
            `${USER_BASE_PATH}/users/director-requests/`,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const acceptDirectorRequest = async (requestId, token) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/users/director-requests/accept/${requestId}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const rejectDirectorRequest = async (requestId, token) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/users/director-requests/reject/${requestId}`,
            {},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const sendLinkToPlayerRequest = async (token, formData) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/users/link-player-requests/`,
            formData,
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};
