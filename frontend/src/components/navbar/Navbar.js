import { useContext } from "react";
import "./navbar.scss";

import { Link } from "react-router-dom";
import { AuthContext } from "../contexts/authContext";

export const Navbar = () => {
    const { token, user } = useContext(AuthContext);

    return (
        <div className="navbar">
            <div className="wrapper">
                <div className="left">
                    <Link to="/">
                        <img src="/images/matchscore.png" alt="logo" />
                    </Link>
                </div>
                <div className="right">
                    {token ? (
                        <Link className="link" to={`/profile/${user.id}`}>
                            Profile
                        </Link>
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
