import axios from "axios";
import { USER_BASE_PATH } from "../routes/paths";

export const sendPlayerRequest = async (userId, token, playerData) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/players/${userId}/player-request`,
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

export const getPlayerRequests = async (token) => {
    try {
        const response = await axios.get(`${USER_BASE_PATH}/players/requests`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};



export const acceptPlayerRequest = async (requestId, token) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/players/requests/accept/${requestId}`,
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

export const rejectPlayerRequest = async (requestId, token) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/players/requests/reject/${requestId}`,
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
