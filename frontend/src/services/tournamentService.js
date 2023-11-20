import axios from "axios";
import { BASE_PATH } from "../routes/paths";

export const create = async (tournamentData, token) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/tournaments/`,
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
        const response = await axios.get(`${BASE_PATH}/tournaments/`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getOne = async (tournamentId) => {
    try {
        const response = await axios.get(
            `${BASE_PATH}/tournaments/${tournamentId}`
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};
