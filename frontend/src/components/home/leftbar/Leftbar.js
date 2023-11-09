import "./leftbar.scss";

import { useContext } from "react";
import { AuthContext } from "../../../contexts/authContext";
import { Link } from "react-router-dom";

import { TOURNAMENTS } from "../../../routes/routes";

export const Leftbar = () => {
    const { user, token } = useContext(AuthContext);

    return (
        <div className="leftbar">
            <div className="leftbarWrapper">
                <Link
                    className="link"
                    to={TOURNAMENTS}
                    user={user}
                    token={token}
                >
                    Tournaments
                </Link>
                <ul className="leftbarList">
                    <li className="leftbarListItem">
                        <span>Champions League</span>
                        <span>All stars</span>
                        <span>Grand Prix</span>
                    </li>
                </ul>

                <Link className="link" to={TOURNAMENTS}>
                    Sports
                </Link>

                <ul className="leftbarList">
                    <li className="leftbarListItem">
                        <span>Football</span>
                        <span>Basketball</span>
                        <span>Volleyball</span>
                        <span>Baseball</span>
                        <span>Tennis</span>
                        <span>Box</span>
                        <span>America Football</span>
                    </li>
                </ul>
            </div>
        </div>
    );
};
