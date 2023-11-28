import axios from "axios";
import { BASE_PATH } from "../routes/paths";

export const createKnockout = async (tournamentData, token) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/tournaments/knockout`,
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

export const createLeague = async (tournamentData, token) => {
    try {
        const response = await axios.post(
            `${BASE_PATH}/tournaments/league`,
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

export const getAll = async (page) => {
    try {
        const response = await axios.get(`${BASE_PATH}/tournaments/`, {
            params: { page: page },
        });
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

export const getKnockoutRounds = async (tournamentId) => {
    try {
        const response = await axios.get(
            `${BASE_PATH}/tournaments/${tournamentId}/rounds`
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const startKnockoutTournament = async (
    tournamentId,
    token,
    startDate
) => {
    try {
        const response = await axios.put(
            `${BASE_PATH}/tournaments/${tournamentId}/knockout_start`,
            startDate,
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

export const getLeagueStandings = async (tournamentId) => {
    try {
        const response = await axios.get(
            `${BASE_PATH}/tournaments/${tournamentId}/points`
        );
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const updateStartDate = async (tournamentId, token, startDate) => {
    try {
        const response = await axios.put(
            `${BASE_PATH}/tournaments/${tournamentId}/date`,
            startDate,
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

export const updatePlayers = async (tournamentId, token, players) => {
    try {
        const response = await axios.put(
            `${BASE_PATH}/tournaments/${tournamentId}/players`,
            players,
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

export const getPlayersByTournamentId = async (tournamentId, token) => {
    try {
        const response = await axios.get(
            `${BASE_PATH}/tournaments/${tournamentId}/players`,
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

export const getWeather = async (location) => {
    const city = location?.split(", ")[0].trim();

    try {
        const response = await axios.get(`${BASE_PATH}/weather/`, {
            params: { location: city },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};
