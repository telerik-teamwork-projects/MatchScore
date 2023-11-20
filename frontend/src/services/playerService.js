import axios from "axios";
import { BASE_PATH } from "../routes/paths";

export const getAll = async (page) => {
    try {
        const response = await axios.get(`${BASE_PATH}/players/`, {
            params: { page: page },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getOne = async (playerId) => {
    try {
        const response = await axios.get(`${BASE_PATH}/players/${playerId}/`);
        return response.data;
    } catch (error) {
        throw error;
    }
};
