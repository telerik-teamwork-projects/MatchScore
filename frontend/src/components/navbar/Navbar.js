import "./navbar.scss";

import { useContext, useState } from "react";
import { LogoutConfirmation } from "../logout/LogoutConfirmation";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../contexts/authContext";
import { LOGIN } from "../../routes/routes";
import { Search } from "@mui/icons-material";
import { getUsers } from "../../services/authService";
import { getPlayerRequests } from "../../services/playerService";
import { UserSearchModal } from "../userSearch/UserSearchModal";
import { PlayerRequests } from "../playerRequests/PlayerRequests";

export const Navbar = () => {
    const { token, user, userLogout } = useContext(AuthContext);
    const navigate = useNavigate();

    const [logoutWindow, setLogoutWindow] = useState(null);

    const [showUsersSearch, setShowUsersSearch] = useState(false);
    const [userSearchResults, setUserSearchResults] = useState(null);

    const [notifiacationsModalOpen, setNotificationsModalOpen] =
        useState(false);
    const [notificationsResult, setNotificationsResult] = useState(null);

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

    const closeMotificationsModal = () => {
        setNotificationsModalOpen(false);
    };

    const onNotifications = async (e) => {
        e.preventDefault();

        try {
            const result = await getPlayerRequests(token);
            setNotificationsResult(result);
            setNotificationsModalOpen(true);
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
                                        <button
                                            className="navbarNotifications"
                                            onClick={(e) => onNotifications(e)}
                                        >
                                            Notifications
                                        </button>
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
            {notifiacationsModalOpen && (
                <PlayerRequests
                    requests={notificationsResult}
                    setRequests={setNotificationsResult}
                    onClose={closeMotificationsModal}
                    token={token}
                />
            )}
        </>
    );
};
