import axios from "axios";
import { BASE_PATH } from "../routes/paths";

export const sendDirectorRequest = async (userId, userEmail, token) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/requests/director-requests/`,
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
            `${BASE_PATH}/requests/director-requests/`,
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
            `${BASE_PATH}/requests/director-requests/accept/${requestId}/`,
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
            `${BASE_PATH}/requests/director-requests/reject/${requestId}/`,
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
            `${BASE_PATH}/requests/link-player-requests/`,
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

export const getLinkPlayerRequests = async (token) => {
    try {
        const response = await axios.get(
            `${BASE_PATH}/requests/link-player-requests/`,
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

export const acceptLinkPlayerRequest = async (requestId, token) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/requests/link-player-requests/accept/${requestId}/`,
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

export const rejectLinkPlayerRequest = async (requestId, token) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/requests/link-player-requests/reject/${requestId}/`,
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

export const sendTournamentRequestNoPlayer = async (
    tournamentId,
    token,
    playerData
) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/requests/tournament-requests/${tournamentId}/`,
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

export const sendTournamentRequestWithPlayer = async (
    tournamentId,
    token,
    playerData
) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/requests/tournament-requests/${tournamentId}/existing/`,
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

export const getTournamentRequests = async (tournamentId, token) => {
    try {
        const response = await axios.get(
            `${BASE_PATH}/requests/tournament-requests/${tournamentId}/`,
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

export const acceptTournamentRequest = async (requestId, token) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/requests/tournament-requests/accept/${requestId}/`,
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

export const rejectTournamentRequest = async (requestId, token) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/requests/tournament-requests/reject/${requestId}/`,
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

export const sendPlayerRequest = async (userId, token, playerData) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/requests/player-request/${userId}/`,
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
        const response = await axios.get(
            `${BASE_PATH}/requests/player-requests/`,
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

export const acceptPlayerRequest = async (requestId, token) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/requests/player-requests/accept/${requestId}/`,
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
            `${BASE_PATH}/requests/player-requests/reject/${requestId}/`,
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
