import "./navbar.scss";

import { useContext, useState } from "react";
import { LogoutConfirmation } from "../logout/LogoutConfirmation";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../contexts/authContext";
import { LOGIN } from "../../routes/routes";
import { Search } from "@mui/icons-material";
import { getLinkNotifications, getUsers } from "../../services/authService";
import { getPlayerRequests } from "../../services/playerService";
import { getDirectorRequests } from "../../services/authService";
import { UserSearchModal } from "../userSearch/UserSearchModal";
import { PlayerRequests } from "../playerRequests/PlayerRequests";
import { Notifications } from "@mui/icons-material";
import Work from "@mui/icons-material/Work";
import PeopleIcon from "@mui/icons-material/People";
import { DirectorRequests } from "../directorRequests/DirectorRequests";
import { LinkPlayerRequests } from "../linkPlayerRequeests/LinkPlayerRequests";

export const Navbar = () => {
    const { token, user, userLogout } = useContext(AuthContext);
    const navigate = useNavigate();

    const [logoutWindow, setLogoutWindow] = useState(null);

    const [showUsersSearch, setShowUsersSearch] = useState(false);
    const [userSearchResults, setUserSearchResults] = useState(null);

    const [playerNotificationsModalOpen, setPlayerNotificationsModalOpen] =
        useState(false);
    const [playerNotificationsResult, setPlayerNotificationsResult] =
        useState(null);

    const [
        directorNotificacationsModalOpen,
        setDirectorNotificationsModalOpen,
    ] = useState(false);
    const [directorNotificationsResult, setDirectorNotificationsResult] =
        useState(null);

    const [linkNotificationsModalOpen, setLinkNotificationsModalOpen] =
        useState(false);
    const [linkNotificationsResult, setLinkNotificationsResult] =
        useState(null);

    const [searchQ, setSearchQ] = useState({
        search: "",
    });

    const onChange = (e) =>
        setSearchQ({ ...searchQ, [e.target.name]: e.target.value });

    const onLogout = () => {
        setLogoutWindow(true);
    };

    const confirmLogout = async () => {
        await userLogout();
        setLogoutWindow(false);
        navigate(LOGIN);
    };

    const cancelLogout = () => {
        setLogoutWindow(false);
    };

    const onSearch = async (e) => {
        e.preventDefault();
        setShowUsersSearch(true);

        try {
            const userData = await getUsers(searchQ);
            setUserSearchResults(userData);
        } catch (error) {
            console.error(error);
        }
    };

    const closePlayerNotifications = () => {
        setPlayerNotificationsModalOpen(false);
    };

    const closeDirectorNotifications = () => {
        setDirectorNotificationsModalOpen(false);
    };

    const closeLinkNotifications = () => {
        setLinkNotificationsModalOpen(false);
    };

    const onPlayerNotifications = async (e) => {
        e.preventDefault();

        try {
            const result = await getPlayerRequests(token);
            setPlayerNotificationsResult(result);
            setPlayerNotificationsModalOpen(true);
        } catch (error) {
            console.error(error);
        }
    };

    const onDirectorNotifications = async (e) => {
        e.preventDefault();

        try {
            const result = await getDirectorRequests(token);
            setDirectorNotificationsResult(result);
            setDirectorNotificationsModalOpen(true);
        } catch (error) {
            console.error(error);
        }
    };

    const onLinkNotifications = async (e) => {
        e.preventDefault();

        try {
            const result = await getLinkNotifications(token);
            setLinkNotificationsResult(result);
            setLinkNotificationsModalOpen(true);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <>
            <div className="navbar">
                <div className="navbarWrapper">
                    <div className="navbarLeft">
                        <Link to="/">
                            <img src="/images/logo/matchscore.png" alt="logo" />
                        </Link>
                    </div>
                    <div className="navbarCenter">
                        <form
                            onSubmit={(e) => onSearch(e)}
                            className="searchbar"
                        >
                            <Search className="searchIcon" />
                            <input
                                placeholder="Search for users, tournaments and more ..."
                                className="searchInput"
                                type="text"
                                name="search"
                                value={searchQ.search}
                                onChange={(e) => onChange(e)}
                            />
                        </form>
                    </div>
                    <div className="navbarRight">
                        <div className="navbarRightInfo">
                            {token ? (
                                <>
                                    {user?.role === "admin" && (
                                        <>
                                            <PeopleIcon
                                                className="navbarNotifications"
                                                onClick={(e) =>
                                                    onLinkNotifications(e)
                                                }
                                            />
                                            <Work
                                                className="navbarNotifications"
                                                onClick={(e) =>
                                                    onDirectorNotifications(e)
                                                }
                                            />
                                            <Notifications
                                                className="navbarNotifications"
                                                onClick={(e) =>
                                                    onPlayerNotifications(e)
                                                }
                                            />
                                        </>
                                    )}
                                    <Link
                                        className="navbarRightLink"
                                        to={`/profile/${user.id}`}
                                    >
                                        Profile
                                    </Link>
                                    <Link
                                        className="navbarRightLink"
                                        onClick={onLogout}
                                    >
                                        Logout
                                    </Link>
                                    {logoutWindow && (
                                        <LogoutConfirmation
                                            isOpen={logoutWindow}
                                            onConfirm={confirmLogout}
                                            onCancel={cancelLogout}
                                        />
                                    )}
                                    {showUsersSearch && userSearchResults && (
                                        <UserSearchModal
                                            users={userSearchResults}
                                            onClose={() =>
                                                setShowUsersSearch(false)
                                            }
                                        />
                                    )}
                                </>
                            ) : (
                                <Link className="navbarRightLink" to="/login">
                                    Login
                                </Link>
                            )}
                        </div>
                    </div>
                </div>
            </div>
            {playerNotificationsModalOpen && (
                <PlayerRequests
                    requests={playerNotificationsResult}
                    setRequests={setPlayerNotificationsResult}
                    onClose={closePlayerNotifications}
                    token={token}
                />
            )}
            {directorNotificacationsModalOpen && (
                <DirectorRequests
                    requests={directorNotificationsResult}
                    setRequests={setDirectorNotificationsResult}
                    onClose={closeDirectorNotifications}
                    token={token}
                />
            )}
            {linkNotificationsModalOpen && (
                <LinkPlayerRequests
                    requests={linkNotificationsResult}
                    setRequests={setLinkNotificationsResult}
                    onClose={closeLinkNotifications}
                    token={token}
                />
            )}
        </>
    );
};
