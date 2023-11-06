import "./navbar.scss";

import { Link } from "react-router-dom";

export const Navbar = () => {
    return (
        <div className="navbar">
            <div className="wrapper">
                <div className="left">
                    <img src="/images/matchscore.png" alt="logo" />
                </div>
                <div className="right">
                    <Link className="link" to="/login">
                        Login
                    </Link>
                </div>
            </div>
        </div>
    );
};
