import axios from "axios";
import { BASE_PATH } from "../routes/paths";

export const updateMatchScore = async (matchId, matchScores, token) => {
    try {
        const response = await axios.put(
            `${BASE_PATH}/matches/${matchId}/score`,
            matchScores[0].participants,
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
