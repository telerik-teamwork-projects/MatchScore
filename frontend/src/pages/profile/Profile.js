import "./profile.scss";

import { useContext, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { AuthContext } from "../../contexts/authContext";
import { Leftbar } from "../../components/home/leftbar/Leftbar";
import { getUser, deleteUser } from "../../services/authService";
import { HOME, PROFILE } from "../../routes/routes";
import { USER_BASE_PATH } from "../../routes/paths";
import { DeleteUserConfirmation } from "../../components/userDelete/DeleteUserConfirmation";

export const Profile = () => {
    const navigate = useNavigate();
    const { userId } = useParams();
    const { token, user } = useContext(AuthContext);
    const [profile, setProfile] = useState(null);
    const [deleteConfirmation, setDeleteConfirmation] = useState(false);

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

    const onDelete = () => {
        setDeleteConfirmation(true);
    };

    const confirmDelete = async () => {
        await deleteUser(userId);
        setDeleteConfirmation(false);
        navigate(HOME);
    };

    const cancelDelete = () => {
        setDeleteConfirmation(false);
    };

    return (
        <>
            <div className="profile">
                <Leftbar />
                <div className="profileRight">
                    <div className="profileRightTop">
                        <div className="profileCover">
                            {profile?.cover_img ? (
                                <img
                                    className="profileCoverImg"
                                    src={`${USER_BASE_PATH}${profile?.cover_img}`}
                                    alt={profile?.username}
                                />
                            ) : (
                                <img
                                    className="profileCoverImg"
                                    src="/images/avatar/default_cover.jpg"
                                    alt={profile?.username}
                                />
                            )}

                            {profile?.profile_img ? (
                                <img
                                    className="profileUserImg"
                                    src={`${USER_BASE_PATH}${profile?.profile_img}`}
                                    alt=""
                                />
                            ) : (
                                <img
                                    className="profileUserImg"
                                    src="/images/avatar/default.jpg"
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
                                <Link
                                    className="profileDeleteBtn"
                                    onClick={onDelete}
                                >
                                    Delete
                                </Link>
                            </div>
                        )}
                        {deleteConfirmation && (
                            <DeleteUserConfirmation
                                isOpen={deleteConfirmation}
                                onConfirm={confirmDelete}
                                onCancel={cancelDelete}
                            />
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