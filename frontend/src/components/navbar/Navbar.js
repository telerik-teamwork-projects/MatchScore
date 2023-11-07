import { useContext, useState } from "react";
import "./navbar.scss";
import { LogoutConfirmation } from "../logout/LogoutConfirmation";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/authContext";
import { LOGIN } from "../../routes/routes";

export const Navbar = () => {
    const { token, user, userLogout } = useContext(AuthContext);
    const navigate = useNavigate();

    const [logoutWindow, setLogoutWindow] = useState(null);

    const onLogout = async () => {
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

    return (
        <div className="navbar">
            <div className="navbarWrapper">
                <div className="navbarLeft">
                    <Link to="/">
                        <img src="/images/matchscore.png" alt="logo" />
                    </Link>
                </div>
                <div className="navbarRight">
                    {token ? (
                        <>
                            <Link className="link" to={`/profile/${user.id}`}>
                                Profile
                            </Link>
                            <Link className="link" onClick={onLogout}>
                                Logout
                            </Link>
                            {logoutWindow && (
                                <LogoutConfirmation
                                    isOpen={logoutWindow}
                                    onConfirm={confirmLogout}
                                    onCancel={cancelLogout}
                                />
                            )}
                        </>
                    ) : (
                        <Link className="link" to="/login">
                            Login
                        </Link>
                    )}
                </div>
            </div>
        </div>
    );
};
