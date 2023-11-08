import "./profile.scss";

import { useContext, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { AuthContext } from "../../components/contexts/authContext";
import { Leftbar } from "../../components/home/leftbar/Leftbar";
import { getUser } from "../../services/authService";

export const Profile = () => {
    const { userId } = useParams();
    const { token } = useContext(AuthContext);
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
                            <img
                                className="profileUserImg"
                                src="/images/teams/liverpool.png"
                                alt=""
                            />
                        </div>
                        <div className="profileInfo">
                            <h4 className="profileInfoName">
                                {profile?.username}
                            </h4>
                            <span className="profileInfoDesc">
                                {profile?.email}
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
