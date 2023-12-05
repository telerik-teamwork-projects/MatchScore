import "./playerProfile.scss";

import { useContext, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Leftbar } from "../../components/home/leftbar/Leftbar";
import { getOne, getAchievements } from "../../services/playerService";
import { BASE_PATH } from "../../routes/paths";
import { Rightbar } from "../home/rightbar/Rightbar";
import { AuthContext } from "../../contexts/authContext";
import { PLAYERS, PROFILE } from "../../routes/routes";

export const PlayerProfile = () => {
    const { playerId } = useParams();
    const { user } = useContext(AuthContext);
    const [playerProfile, setPlayerProfile] = useState(null);
    const [playerAchievements, setPlayerAchievements] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getOne(playerId);
                setPlayerProfile(userData);
                const achievementsData = await getAchievements(playerId);
                setPlayerAchievements(achievementsData);
            } catch (error) {
                console.error(error);
            }
        };
        fetchUser();
    }, [playerId]);

    return (
        <>
            <div className="playerProfile">
                <Leftbar />
                <div className="playerProfileFeed">
                    <div className="playerProfileTop">
                        <div className="playerProfileCover">
                            <img
                                className="playerProfileCoverImg"
                                src="/images/avatar/default_cover.jpg"
                                alt={playerProfile?.full_name}
                            />

                            {playerProfile?.profile_img ? (
                                <img
                                    className="playerProfileImg"
                                    src={`${BASE_PATH}${playerProfile?.profile_img}`}
                                    alt=""
                                />
                            ) : (
                                <img
                                    className="playerProfileImg"
                                    src="/images/avatar/default.jpg"
                                    alt=""
                                />
                            )}
                        </div>
                        {(playerProfile?.user_id === user?.id ||
                            user?.role === "admin" ||
                            (!playerProfile?.user_id &&
                                user?.role === "director")) && (
                            <div className="playerProfileBtns">
                                <Link
                                    to={`${PLAYERS}/${playerId}/update`}
                                    className="playerProfileEditBtn"
                                >
                                    Edit
                                </Link>
                                {/* <Link
                                    className="playerProfileDeleteBtn"
                                    // onClick={onDelete}
                                >
                                    Delete
                                </Link> */}
                            </div>
                        )}
                        {playerProfile?.user_id && (
                            <div className="playerProfileViewUserBtns">
                                <Link
                                    to={`${PROFILE}/${playerProfile?.user_id}`}
                                >
                                    <button className="playerProfileViewUserBtn">
                                        View User Profile
                                    </button>
                                </Link>
                            </div>
                        )}
                        <div className="playerProfileInfo">
                            <h4 className="playerProfileInfoName">
                                {playerProfile?.full_name}
                            </h4>
                        </div>
                    </div>
                    <div className="playerProfileBottom">
                        <div className="playerProfileBottomLeft">
                            <div className="playerProfileWrapper">
                                <h3>Player Info</h3>
                                <div className="playerMain">
                                    <div className="playerMainFullName">
                                        <p>Full Name:</p>
                                        <span>
                                            {playerProfile?.full_name || "N/A"}
                                        </span>
                                    </div>
                                    <div className="playerMainCountry">
                                        <p>Country:</p>
                                        <span>
                                            {playerProfile?.country || "N/A"}
                                        </span>
                                    </div>
                                    <div className="playerMainSportsClub">
                                        <p>Sports Club:</p>
                                        <span>
                                            {playerProfile?.sports_club ||
                                                "N/A"}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="playerProfileBottomRight">
                            <div className="playerAchievementsWrapper">
                                <h3>Player Achievements</h3>

                                <div className="playerTournaments">
                                    <p>Tournaments Played</p>
                                    <span>
                                        {playerAchievements?.tournaments_played ||
                                            "N/A"}
                                    </span>
                                </div>

                                <div className="playerTournaments">
                                    <p>Tournaments Won</p>
                                    <span>
                                        {playerAchievements?.tournaments_won ||
                                            "N/A"}
                                    </span>
                                </div>
                                <div className="playerTournaments">
                                    <p>Matches Played</p>
                                    <span>
                                        {playerAchievements?.matches_played ||
                                            "N/A"}
                                    </span>
                                </div>
                                <div className="playerMatches">
                                    <p>Matches Won</p>
                                    <span>
                                        {playerAchievements?.matches_won ||
                                            "N/A"}
                                    </span>{" "}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <Rightbar />
            </div>
        </>
    );
};
