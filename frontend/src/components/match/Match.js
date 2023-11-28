import "./match.scss";
import { useContext, useState } from "react";
import { Link } from "react-router-dom";

import { AuthContext } from "../../contexts/authContext";

import { updateMatchScore } from "../../services/matchesService";

import { PLAYERS, TOURNAMENTS } from "../../routes/routes";
import { BASE_PATH } from "../../routes/paths";

export const Match = ({ match }) => {
    const { user, token } = useContext(AuthContext);
    const [scores, setScores] = useState({
        score1: match?.score[0]?.score,
        score2: match?.score[1]?.score,
    });

    if (!match || !match.score || match.score.length < 2) {
        return null;
    }

    const matchDate = new Date(match.date);

    const dateOptions = {
        year: "numeric",
        month: "numeric",
        day: "numeric",
    };

    const timeOptions = {
        hour: "numeric",
        minute: "numeric",
        hour12: true,
    };

    const formattedDate = matchDate.toLocaleString(undefined, dateOptions);
    const formattedTime = matchDate.toLocaleString(undefined, timeOptions);

    const handleScoreChange = (playerIndex, e) => {
        const newScores = {
            ...scores,
            [`score${playerIndex + 1}`]: e.target.value,
        };
        setScores(newScores);
    };

    const handleUpdateScore = async () => {
        const matchId = match.id;
        const matchScores = {
            matches: [
                {
                    participants: [
                        {
                            player_id: match.score[0].player_id,
                            player: match.score[0].player,
                            score: Number(scores.score1),
                        },
                        {
                            player_id: match.score[1].player_id,
                            player: match.score[1].player,
                            score: Number(scores.score2),
                        },
                    ],
                },
            ],
        };
        try {
            await updateMatchScore(matchId, matchScores.matches, token);
            window.location.reload();
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="matchBox">
            <div className="matchHeader">
                <div className="matchHeaderLeft">
                    <span>Live</span>
                </div>
                <div className="matchHeaderRight">
                    <span>
                        {formattedDate}, {formattedTime}
                    </span>
                </div>
            </div>
            <hr />
            <div className="matchMain">
                <Link
                    className="link"
                    to={`${TOURNAMENTS}/${match?.tournament_id}`}
                >
                    <span className="matchTitle">
                        {match?.tournament_title}
                    </span>
                </Link>
                <div className="matchTeam">
                    <div className="teamInfo">
                        {match?.score[0].profile_img ? (
                            <img
                                src={`${BASE_PATH}${match?.score[0].profile_img}`}
                                alt=""
                            />
                        ) : (
                            <img src="/images/avatar/default.jpg" alt="team1" />
                        )}
                        <Link
                            className="link"
                            to={`${PLAYERS}/${match?.score[0].player_id}`}
                        >
                            <span className="Team1">
                                {match?.score[0].player}
                            </span>
                        </Link>
                    </div>
                    {user?.role === "admin" || user?.role === "director" ? (
                        <input
                            name="score1"
                            type="number"
                            value={scores.score1}
                            onChange={(e) => handleScoreChange(0, e)}
                        />
                    ) : (
                        <span className="teamScore">
                            {match?.score[0].score}
                        </span>
                    )}
                </div>
                <div className="matchTeam">
                    <div className="teamInfo">
                        {match?.score[1].profile_img ? (
                            <img
                                src={`${BASE_PATH}${match?.score[1].profile_img}`}
                                alt=""
                            />
                        ) : (
                            <img src="/images/avatar/default.jpg" alt="team2" />
                        )}
                        <Link
                            className="link"
                            to={`${PLAYERS}/${match?.score[1].player_id}`}
                        >
                            <span className="Team1">
                                {match?.score[1].player}
                            </span>
                        </Link>
                    </div>
                    {user?.role === "admin" || user?.role === "director" ? (
                        <input
                            name="score2"
                            type="number"
                            value={scores.score2}
                            onChange={(e) => handleScoreChange(1, e)}
                        />
                    ) : (
                        <span className="teamScore">
                            {match?.score[1].score}
                        </span>
                    )}
                </div>
            </div>
            <hr />
            <div className="matchBottom">
                {(user?.role === "admin" || user?.role === "director") && (
                    <button
                        className="actionButton"
                        onClick={handleUpdateScore}
                    >
                        Update Score
                    </button>
                )}
                <button className="actionButton">Watch Live</button>
            </div>
        </div>
    );
};
