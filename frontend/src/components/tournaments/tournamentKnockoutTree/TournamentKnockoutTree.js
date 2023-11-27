import React, { useContext, useEffect, useState } from "react";
import { getKnockoutRounds } from "../../../services/tournamentService";
import "./tournamentKnockoutTree.scss";
import { updateMatchScore } from "../../../services/matchesService";
import { AuthContext } from "../../../contexts/authContext";

export const TournamentKnockoutTree = ({ tournamentId, token }) => {
    const { user } = useContext(AuthContext);

    const [tournamentData, setTournamentData] = useState([]);

    useEffect(() => {
        const fetchTournamentData = async () => {
            try {
                const response = await getKnockoutRounds(tournamentId);
                setTournamentData(response.rounds || []);
            } catch (error) {
                console.error("Error fetching tournament data:", error);
            }
        };

        fetchTournamentData();
    }, [tournamentId]);

    const updateScore = (
        roundIndex,
        matchIndex,
        participantIndex,
        newScore
    ) => {
        setTournamentData((prevData) => {
            const newData = [...prevData];
            newData[roundIndex].matches[matchIndex].participants[
                participantIndex
            ].score = newScore;
            return newData;
        });
    };

    const handleScoreChange = (e, roundIndex, matchIndex, participantIndex) => {
        const newScore = e.target.value;
        updateScore(roundIndex, matchIndex, participantIndex, newScore);
    };

    const handleUpdateScore = async (
        roundIndex,
        matchIndex,
        participant1,
        participant2
    ) => {
        const matchId = tournamentData[roundIndex].matches[matchIndex].match_id;
        const matchScores = {
            matches: [
                {
                    participants: [
                        {
                            player_id: participant1?.id,
                            player: participant1?.player,
                            score: Number(participant1?.score),
                        },
                        {
                            player_id: participant2?.id,
                            player: participant2?.player,
                            score: Number(participant2?.score),
                        },
                    ],
                },
            ],
        };

        try {
            await updateMatchScore(matchId, matchScores.matches, token);
            window.location.reload();
        } catch (error) {
            console.error("Error updating match score:", error);
        }
    };
    return (
        <div id="bracket">
            {tournamentData.map((round, roundIndex) => (
                <div key={roundIndex} className={`round round-${round.round}`}>
                    <div className="round-details">
                        {round.round}
                        <br />
                    </div>

                    {round.matches.map((match, matchIndex) => (
                        <ul key={match.match_id} className="matchup">
                            <li className="team team-top">
                                {match.participants[0] && (
                                    <>
                                        {match.participants[0].player}
                                        {user?.role === "admin" ||
                                        user?.role === "director" ? (
                                            <input
                                                type="number"
                                                value={
                                                    match.participants[0]
                                                        .score || 0
                                                }
                                                onChange={(e) =>
                                                    handleScoreChange(
                                                        e,
                                                        roundIndex,
                                                        matchIndex,
                                                        0
                                                    )
                                                }
                                            />
                                        ) : (
                                            <span>
                                                {match.participants[0].score}
                                            </span>
                                        )}
                                    </>
                                )}
                            </li>
                            <li className="team team-bottom">
                                {match.participants[1] && (
                                    <>
                                        {match.participants[1].player}
                                        {user?.role === "admin" ||
                                        user?.role === "director" ? (
                                            <input
                                                type="number"
                                                value={
                                                    match.participants[1]
                                                        .score || 0
                                                }
                                                onChange={(e) =>
                                                    handleScoreChange(
                                                        e,
                                                        roundIndex,
                                                        matchIndex,
                                                        1
                                                    )
                                                }
                                            />
                                        ) : (
                                            <span>
                                                {match.participants[1].score}
                                            </span>
                                        )}
                                    </>
                                )}
                            </li>
                            {(user?.role === "admin" ||
                                user?.role === "director") && (
                                <button
                                    onClick={() =>
                                        handleUpdateScore(
                                            roundIndex,
                                            matchIndex,
                                            match.participants[0],
                                            match.participants[1]
                                        )
                                    }
                                >
                                    Update Score
                                </button>
                            )}
                        </ul>
                    ))}
                </div>
            ))}
        </div>
    );
};
