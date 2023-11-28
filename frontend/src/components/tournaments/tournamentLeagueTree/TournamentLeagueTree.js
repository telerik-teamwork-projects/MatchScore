import "./tournamentLeagueTree.scss";

import { useState, useEffect } from "react";

import { getLeagueStandings } from "../../../services/tournamentService";
import { getMatchesByTournamentId } from "../../../services/matchesService";

import { Link } from "react-router-dom";
import { PLAYERS } from "../../../routes/routes";
import { Pagination } from "../../pagination/Pagination";
import { Match } from "../../match/Match";

export const TournamentLeagueTree = ({ tournamentId }) => {
    const [standings, setStandings] = useState(null);
    const [matchesData, setMatchesData] = useState({
        matches: [],
        pagination: {
            page: 1,
            items_per_page: 10,
            total_pages: 1,
        },
    });

    const [showStandings, setShowStandings] = useState(null);
    const [showMatches, setShowMatches] = useState(null);

    const openShowStandings = async () => {
        try {
            const standingsData = await getLeagueStandings(tournamentId);
            setStandings(standingsData);
        } catch (error) {
            console.log(error);
        }
        setShowStandings(true);
        setShowMatches(false);
    };

    const openShowMatches = async (page) => {
        try {
            const pageNumber = typeof page === "object" ? 1 : page;
            const matchesData = await getMatchesByTournamentId(
                pageNumber,
                tournamentId
            );
            setMatchesData(matchesData);
        } catch (error) {
            console.log(error);
        }
        setShowStandings(false);
        setShowMatches(true);
    };

    useEffect(() => {
        openShowMatches(matchesData.pagination.page);
    }, [matchesData.pagination.page]);

    const handlePageChange = (pageNumber) => {
        openShowMatches(pageNumber);
        window.scrollTo({ top: 0, behavior: "smooth" });
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
            {showMatches && (
                <div className="matchesContainer">
                    {matchesData?.matches ? (
                        <>
                            <div className="match">
                                {matchesData?.matches.map((match) => (
                                    <Match match={match} key={match.id} />
                                ))}
                            </div>
                            <Pagination
                                handlePageChange={handlePageChange}
                                dataToFetch={matchesData}
                            />
                        </>
                    ) : (
                        <p>Loading matches...</p>
                    )}
                </div>
            )}

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
