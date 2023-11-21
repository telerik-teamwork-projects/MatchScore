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

export const playerUpdate = async (playerId, token, formData) => {
    try {
        const formDataToSend = new FormData();
        formDataToSend.append("full_name", formData.full_name);
        formDataToSend.append("country", formData.country);
        formDataToSend.append("sports_club", formData.sports_club);
        formDataToSend.append("profile_img", formData.profile_img);

        const response = await axios.put(
            `${BASE_PATH}/players/${playerId}/update/`,
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
