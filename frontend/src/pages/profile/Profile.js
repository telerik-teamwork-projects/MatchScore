import "./profile.scss";

import { useContext, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { AuthContext } from "../../contexts/authContext";
import { Leftbar } from "../../components/home/leftbar/Leftbar";
import { getUser } from "../../services/authService";
import { PROFILE } from "../../routes/routes";
import { USER_BASE_PATH } from "../../routes/paths";

export const Profile = () => {
    const { userId } = useParams();
    const { token, user } = useContext(AuthContext);
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getUser(userId, token);
                setProfile(userData);
            } catch (error) {
                console.error(error);
            }
        };
        fetchUser();
    }, [userId, token]);

    return (
        <>
            <div className="profile">
                <Leftbar />
                <div className="profileRight">
                    <div className="profileRightTop">
                        <div className="profileCover">
                            <img
                                className="profileCoverImg"
                                src="/images/teams/liverpool.png"
                                alt=""
                            />
                            {profile?.profile_img ? (
                                <img
                                    className="profileUserImg"
                                    src={`${USER_BASE_PATH}${profile?.profile_img}`}
                                    alt=""
                                />
                            ) : (
                                <img
                                    className="profileUserImg"
                                    src="/images/teams/liverpool.png"
                                    alt=""
                                />
                            )}
                        </div>
                        {(profile?.id === user?.id ||
                            user?.role === "admin") && (
                            <div className="profileBtns">
                                <Link
                                    to={`${PROFILE}/${userId}/update`}
                                    className="profileEditBtn"
                                >
                                    Edit
                                </Link>
                                <Link className="profileDeleteBtn">Delete</Link>
                            </div>
                        )}
                        <div className="profileInfo">
                            <h4 className="profileInfoName">
                                {profile?.username}
                            </h4>
                            <span className="profileInfoDesc">
                                {profile?.bio}
                            </span>
                        </div>
                    </div>
                    <div className="profileRightBottom">
                        <p>sdnasda</p>
                    </div>
                </div>
            </div>
        </>
    );
};
