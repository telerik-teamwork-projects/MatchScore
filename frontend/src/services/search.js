import axios from "axios";
import { BASE_PATH } from "../routes/paths";

export const searchUsers = async (searchQ) => {
    try {
        const response = await axios.get(`${BASE_PATH}/search/users-search/`, {
            params: { search: searchQ },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const searchPlayers = async (searchQ) => {
    try {
        const response = await axios.get(
            `${BASE_PATH}/search/players-search/`,
            {
                params: { search: searchQ },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const searchTournaments = async (searchQ) => {
    try {
        const response = await axios.get(
            `${BASE_PATH}/search/tournaments-search/`,
            {
                params: { search: searchQ },
            }
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};
