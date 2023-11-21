import "./navbar.scss";

import { useContext, useState } from "react";
import { LogoutConfirmation } from "../logout/LogoutConfirmation";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../contexts/authContext";
import { LOGIN } from "../../routes/routes";
import { Search } from "@mui/icons-material";
import {
    searchUsers,
    searchPlayers,
    searchTournaments,
} from "../../services/searchService";
import {
    getDirectorRequests,
    getLinkPlayerRequests,
    getPlayerRequests,
} from "../../services/requestService";
import { UserSearchModal } from "../search/userSearch/UserSearchModal";
import { PlayerSearchModal } from "../search/playerSearch/PlayerSearchModal";
import { TournamentSearchModal } from "../search/tournamentSearch/TournamentsSearchModal";
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
    const [showPlayersSearch, setShowPlayersSearch] = useState(false);
    const [showTournamentsSearch, setShowTournamentsSearch] = useState(false);

    const [usersSearchResults, setUsersSearchResults] = useState(null);
    const [playersSearchResults, setPlayersSearchResults] = useState(null);
    const [tournamentsSearchResults, setTournamentsSearchResults] =
        useState(null);

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

    const [searchData, setsearchData] = useState({
        search: "",
        category: "users",
    });

    const onChange = (e) => {
        const { name, value } = e.target;
        setsearchData((prevsearchData) => ({
            ...prevsearchData,
            [name]: value,
        }));
    };

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
        if (searchData.category === "users") {
            try {
                const fetchedSearchData = await searchUsers(searchData.search);
                setUsersSearchResults(fetchedSearchData);
                setShowUsersSearch(true);
            } catch (error) {
                console.error(error);
            }
        } else if (searchData.category === "players") {
            try {
                const fetchedSearchData = await searchPlayers(
                    searchData.search
                );
                setPlayersSearchResults(fetchedSearchData);
                setShowPlayersSearch(true);
            } catch (error) {
                console.error(error);
            }
        } else if (searchData.category === "tournaments") {
            try {
                const fetchedSearchData = await searchTournaments(
                    searchData.search
                );
                setTournamentsSearchResults(fetchedSearchData);
                setShowTournamentsSearch(true);
            } catch (error) {
                console.error(error);
            }
        } else {
            console.error("You can search for users, players or tournaments");
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
            const result = await getLinkPlayerRequests(token);
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
                            <div className="searchGroup">
                                <Search className="searchIcon" />
                                <input
                                    placeholder="Search for users, players, and tournaments..."
                                    className="searchInput"
                                    type="text"
                                    name="search"
                                    value={searchData.search}
                                    onChange={(e) => onChange(e)}
                                />
                                <select
                                    className="searchCategory"
                                    name="category"
                                    value={searchData.category}
                                    onChange={(e) => onChange(e)}
                                >
                                    <option value="users">Users</option>
                                    <option value="players">Players</option>
                                    <option value="tournaments">
                                        Tournaments
                                    </option>
                                </select>
                            </div>
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
            {showUsersSearch && (
                <UserSearchModal
                    searchResults={usersSearchResults}
                    onClose={() => setShowUsersSearch(false)}
                />
            )}
            {showPlayersSearch && (
                <PlayerSearchModal
                    searchResults={playersSearchResults}
                    onClose={() => setShowPlayersSearch(false)}
                />
            )}
            {showTournamentsSearch && (
                <TournamentSearchModal
                    searchResults={tournamentsSearchResults}
                    onClose={() => setShowTournamentsSearch(false)}
                />
            )}

            {logoutWindow && (
                <LogoutConfirmation
                    isOpen={logoutWindow}
                    onConfirm={confirmLogout}
                    onCancel={cancelLogout}
                />
            )}
        </>
    );
};
