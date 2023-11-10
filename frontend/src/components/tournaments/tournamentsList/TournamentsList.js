import "./tournamentList.scss";

import { PROFILE } from "../../../routes/routes";
import { MoreVert } from "@mui/icons-material";
import { Link } from "react-router-dom";
// import { USER_BASE_PATH } from "../../../routes/paths";

export const TournamentsList = ({ user, token }) => {
    return (
        <div className="tournamentList">
            <div className="tournamentWrapper">
                <div className="tournamentTop">
                    <div className="tournamentTopLeft">
                        <Link to={`${PROFILE}/${user?.id}`}>
                            <img
                                className="tournamentProfileImg"
                                src="/images/avatar/default.jpg"
                                alt=""
                            />
                        </Link>
                        <div className="tournamentUsernameDateContainer">
                            <span className="tournamentUsername">
                                {user?.username}
                            </span>
                            <span className="tournamentDate">12/12/2023</span>
                        </div>
                    </div>
                    <div className="tournamentTopRight">
                        {user?.id === user?.id && <MoreVert />}
                    </div>
                </div>
                <div className="tournamentCenter">
                    <h2 className="tournamentTitle">title</h2>
                    <div className="tournamentDetails">
                        <div className="tournamentOrgLoc">
                            <span className="tournamentDetail">
                                Organization: Organization,
                            </span>
                            <span className="tournamentDetail">
                                Location: location
                            </span>
                        </div>
                        <div className="tournamentStatusDate">
                            <span className="tournamentDetail">
                                Status: status
                            </span>
                            <span className="tournamentDetail">
                                Date: from - to
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
