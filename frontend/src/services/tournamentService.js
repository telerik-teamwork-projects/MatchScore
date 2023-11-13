import axios from "axios";
import { USER_BASE_PATH } from "../routes/paths";

export const create = async (tournamentData, token) => {
    try {
        const response = await axios.post(
            `${USER_BASE_PATH}/tournaments/`,
            JSON.stringify(tournamentData),
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

export const getAll = async () => {
    try {
        const response = await axios.get(`${USER_BASE_PATH}/tournaments/`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getOne = async (tournamentId) => {
    try {
        const response = await axios.get(
            `${USER_BASE_PATH}/tournaments/${tournamentId}`
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getRequests = async (tournamentId, token) => {
    try {
        const response = await axios.get(
            `${USER_BASE_PATH}/tournaments/${tournamentId}/requests`,
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
