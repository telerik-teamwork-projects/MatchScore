import "./profile.scss";

import { useContext, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { AuthContext } from "../../contexts/authContext";
import { Leftbar } from "../../components/home/leftbar/Leftbar";
import { Rightbar } from "../../components/home/rightbar/Rightbar";
import { getUser, deleteUser } from "../../services/authService";
import { HOME, PLAYERS, PROFILE } from "../../routes/routes";
import { BASE_PATH } from "../../routes/paths";
import { DeleteUserConfirmation } from "../../components/userDelete/DeleteUserConfirmation";
import { RequestBecomePlayer } from "../../components/requestModal/requestBecomePlayer/RequestBecomePlayer";
import { RequestBecomeDirector } from "../../components/requestBecomeDirector/RequestBecomeDirector";
import { RequestLinkWithPlayer } from "../../components/requestLinkWithPlayer/RequestLinkWithPlayer";

export const Profile = () => {
    const navigate = useNavigate();
    const { userId } = useParams();
    const { token, user } = useContext(AuthContext);
    const [profile, setProfile] = useState(null);
    const [deleteConfirmation, setDeleteConfirmation] = useState(false);

    const [becomePlayerModalOpen, setBecomePlayerModalOpen] = useState(false);
    const [becomeDirectorModalOpen, setBecomeDirectorModalOpen] =
        useState(false);
    const [linkWithPlayerModalOpen, setlinkWithPlayerModalOpen] =
        useState(false);

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

    const openBecomePlayer = () => {
        setBecomePlayerModalOpen(true);
    };

    const closeBecomePlayer = () => {
        setBecomePlayerModalOpen(false);
    };

    const openBecomeDirector = () => {
        setBecomeDirectorModalOpen(true);
    };

    const closeBecomeDirector = () => {
        setBecomeDirectorModalOpen(false);
    };

    const openLinkWithPlayer = () => {
        setlinkWithPlayerModalOpen(true);
    };

    const closeLinkWithPlayer = () => {
        setlinkWithPlayerModalOpen(false);
    };

    return (
        <>
            <div className="profile">
                <Leftbar />
                <div className="profileFeed">
                    <div className="profileFeedTop">
                        <div className="profileCover">
                            {profile?.cover_img ? (
                                <img
                                    className="profileCoverImg"
                                    src={`${BASE_PATH}${profile?.cover_img}`}
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
                                    src={`${BASE_PATH}${profile?.profile_img}`}
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
                            <>
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
                                <div className="profileRequestBtns">
                                    <button
                                        className="profileRequestPlayerBtn"
                                        onClick={() => openBecomePlayer()}
                                    >
                                        Player Request
                                    </button>
                                    <button
                                        className="profileRequestPlayerBtn"
                                        onClick={() => openBecomeDirector()}
                                    >
                                        Director Request
                                    </button>
                                    <button
                                        className="profileRequestPlayerBtn"
                                        onClick={() => openLinkWithPlayer()}
                                    >
                                        Link to Player
                                    </button>
                                </div>
                            </>
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
                    {profile?.player && (
                        <div className="profileFeedBottom">
                            <div className="profileFeedBottomLeft">
                                <div className="playerProfileWrapper">
                                    <div className="playerTop">
                                        <h2>Player Profile</h2>
                                    </div>
                                    <div className="playerMain">
                                        <div className="playerMainFullName">
                                            <p>Full Name:</p>
                                            <Link
                                                className="playerMainFullNameLink"
                                                to={`${PLAYERS}/${profile.player.id}`}
                                            >
                                                <span>
                                                    {profile?.player
                                                        .full_name || "N/A"}
                                                </span>
                                            </Link>
                                        </div>
                                        <div className="playerMainCountry">
                                            <p>Country:</p>
                                            <span>
                                                {profile?.player.country ||
                                                    "N/A"}
                                            </span>
                                        </div>
                                        <div className="playerMainSportsClub">
                                            <p>Sports Club:</p>
                                            <span>
                                                {profile?.player.sports_club ||
                                                    "N/A"}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="profileFeedBottomRight">
                                <h2>Achievements</h2>
                            </div>
                        </div>
                    )}
                </div>

                {becomePlayerModalOpen && (
                    <RequestBecomePlayer
                        userId={userId}
                        token={token}
                        onClose={closeBecomePlayer}
                    />
                )}

                {becomeDirectorModalOpen && (
                    <RequestBecomeDirector
                        user={user}
                        token={token}
                        onClose={closeBecomeDirector}
                    />
                )}

                {linkWithPlayerModalOpen && (
                    <RequestLinkWithPlayer
                        userId={userId}
                        token={token}
                        onClose={closeLinkWithPlayer}
                    />
                )}
                <Rightbar />
            </div>
        </>
    );
};
