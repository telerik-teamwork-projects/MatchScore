import { Link } from "react-router-dom";
import "./match.scss";
import { PLAYERS, TOURNAMENTS } from "../../routes/routes";

import { BASE_PATH } from "../../routes/paths";

export const Match = ({ match }) => {
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
                        <Link className="link" to={`${PLAYERS}/${match?.score[0].player_id}`}>
                            <span className="Team1">
                                {match?.score[0].player}
                            </span>
                        </Link>
                    </div>
                    <span className="teamScore">{match?.score[0].score}</span>
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
                        <Link className="link" to={`${PLAYERS}/${match?.score[1].player_id}`}>
                            <span className="Team1">
                                {match?.score[1].player}
                            </span>
                        </Link>
                    </div>
                    <span className="teamScore">{match?.score[1].score}</span>
                </div>
            </div>
            <hr />
            <div className="matchBottom">
                <button className="actionButton">Watch Live</button>
            </div>
        </div>
    );
};
