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
