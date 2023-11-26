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
