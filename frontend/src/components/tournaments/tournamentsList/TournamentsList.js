import "./tournamentList.scss";

import { PROFILE } from "../../../routes/routes";
import { MoreVert } from "@mui/icons-material";
import { Link } from "react-router-dom";
import { USER_BASE_PATH } from "../../../routes/paths";

export const TournamentsList = ({ user, tournaments }) => {
    return (
        <>
            {tournaments?.map((tournament) => (
                <div className="tournamentList" key={tournament.id}>
                    <div className="tournamentWrapper">
                        <div className="tournamentTop">
                            <div className="tournamentTopLeft">
                                <Link to={`${PROFILE}/${tournament.owner.id}`}>
                                    {tournament.owner.profile_img ? (
                                        <img
                                            className="tournamentProfileImg"
                                            src={`${USER_BASE_PATH}${tournament.owner.profile_img}`}
                                            alt=""
                                        />
                                    ) : (
                                        <img
                                            className="tournamentProfileImg"
                                            src="/images/avatar/default.jpg"
                                            alt=""
                                        />
                                    )}
                                </Link>
                                <div className="tournamentUsernameDateContainer">
                                    <span className="tournamentUsername">
                                        {tournament.owner.username}
                                    </span>
                                </div>
                            </div>
                            <div className="tournamentTopRight">
                                {user?.id === tournament.owner.id && (
                                    <MoreVert />
                                )}
                            </div>
                        </div>
                        <div className="tournamentCenter">
                            <h2 className="tournamentTitle">
                                {tournament.title}
                            </h2>
                            <div className="tournamentDetails">
                                <div className="tournamentOrgLoc">
                                    <span className="tournamentDetail">
                                        Organization: {tournament.organization}
                                    </span>
                                    <span className="tournamentDetail">
                                        Location: {tournament.location}
                                    </span>
                                </div>
                                <div className="tournamentStatusDate">
                                    <span className="tournamentDetail">
                                        Status: {tournament.status}
                                    </span>
                                    <span className="tournamentDetail">
                                        Date:{" "}
                                        {tournament.start_date.slice(0, 10)} -{" "}
                                        {tournament.end_date.slice(0, 10)}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </>
    );
};
