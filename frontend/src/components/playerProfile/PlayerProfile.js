import "./playerProfile.scss";

import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Leftbar } from "../../components/home/leftbar/Leftbar";
import { getOne } from "../../services/playerService";
import { BASE_PATH } from "../../routes/paths";
import { Rightbar } from "../home/rightbar/Rightbar";

export const PlayerProfile = () => {
    const { playerId } = useParams();
    const [playerProfile, setPlayerProfile] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getOne(playerId);
                setPlayerProfile(userData);
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

                        <div className="playerProfileInfo">
                            <h4 className="playerProfileInfoName">
                                {playerProfile?.full_name}
                            </h4>
                        </div>
                    </div>
                    <div className="playerProfileBottom">
                        <div className="playerProfileBottomLeft">
                            <div className="playerProfileWrapper">
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
                            <h2>Achievements</h2>
                        </div>
                    </div>
                </div>
                <Rightbar />
            </div>
        </>
    );
};
