import "./tournamentLeagueTree.scss";

import { useState } from "react";

import { getLeagueStandings } from "../../../services/tournamentService";
import { Link } from "react-router-dom";
import { PLAYERS } from "../../../routes/routes";

export const TournamentLeagueTree = ({ tournamentId }) => {
    const [standings, setStandings] = useState(null);

    const [showStandings, setShowStandings] = useState(null);
    const [showMatches, setShowMatches] = useState(null);

    const openShowStandings = async () => {
        try {
            const pointsData = await getLeagueStandings(tournamentId);
            setStandings(pointsData);
        } catch (error) {
            throw error;
        }
        setShowStandings(true);
        setShowMatches(false);
    };

    const openShowMatches = async () => {
        setShowStandings(false);
        setShowMatches(true);
    };

    return (
        <>
            <div className="tournamentButtons">
                <button onClick={openShowMatches} className="matches">
                    Matches
                </button>
                <button onClick={openShowStandings} className="standings">
                    Standings
                </button>
            </div>

            {showStandings && (
                <div className="ptable">
                    <table>
                        <thead className="col">
                            <tr>
                                <th>#</th>
                                <th>Team</th>
                                <th>GP</th>
                                <th>W</th>
                                <th>D</th>
                                <th>L</th>
                                <th>GD</th>
                                <th>PTS</th>
                            </tr>
                        </thead>
                        <tbody>
                            {standings?.players.map((player, index) => (
                                <tr
                                    key={player.player_id}
                                    className={index % 2 === 0 ? "wpos" : "pos"}
                                >
                                    <td>{index + 1}</td>
                                    <td>
                                        <Link
                                            className="link"
                                            to={`${PLAYERS}/${player.player_id}`}
                                        >
                                            {player.full_name}
                                        </Link>
                                    </td>
                                    <td>{player.matches_played}</td>
                                    <td>{player.wins}</td>
                                    <td>{player.draws}</td>
                                    <td>{player.losses}</td>
                                    <td>{player.score_diff}</td>
                                    <td>{player.points}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </>
    );
};
