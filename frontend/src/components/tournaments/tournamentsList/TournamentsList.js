import "./tournamentList.scss";

import { PROFILE, TOURNAMENTS } from "../../../routes/routes";
import { MoreVert } from "@mui/icons-material";
import { Link } from "react-router-dom";
import { USER_BASE_PATH } from "../../../routes/paths";
import { useState } from "react";
import { RequestModal } from "../../requestModal/RequestModal";

export const TournamentsList = ({ user, token, tournaments }) => {
    const [requestWindow, setRequestWindow] = useState(false);
    const [selectedTournament, setSelectedTournament] = useState(null);

    const openRequestModal = (tournament) => {
        setSelectedTournament(tournament);
        setRequestWindow(true);
    };

    const closeRequestModal = () => {
        setSelectedTournament(null);
        setRequestWindow(false);
    };

    return (
        <>
            {tournaments?.map((tournament) => (
                <div className="tournamentList" key={tournament.id}>
                    <div className="tournamentWrapper">
                        <div className="tournamentTop">
                            <div className="tournamentTopLeft">
                                <Link
                                    to={`${PROFILE}/${tournament.owner.id}`}
                                    className="tournamnetTopLeftLink"
                                >
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
                                    <span className="tournamentUsername">
                                        {tournament.owner.username}
                                    </span>
                                </Link>
                            </div>
                            <div className="tournamentTopRight">
                                {user?.id === tournament.owner.id && (
                                    <MoreVert />
                                )}
                            </div>
                        </div>
                        <div className="tournamentCenter">
                            <Link
                                className="tournamentLink"
                                to={`${TOURNAMENTS}/${tournament.id}`}
                            >
                                <h2 className="tournamentTitle">
                                    {tournament.title}
                                </h2>
                            </Link>
                            <div className="tournamentLoc">
                                <p>Location:</p>
                                <span>{tournament.location}</span>
                            </div>
                            <div className="tournamentStatus">
                                <p>Status:</p>
                                <span>{tournament.status}</span>
                            </div>
                            <div className="tournamentDate">
                                <p>Date:</p>
                                <span>
                                    {tournament.start_date.slice(0, 10)} -{" "}
                                    {tournament.end_date.slice(0, 10)}
                                </span>
                            </div>
                        </div>
                        <div className="tournamentBottom">
                            <button
                                className="tournamentJoinBtn"
                                onClick={() => openRequestModal(tournament)}
                            >
                                Request Join
                            </button>
                        </div>
                    </div>
                </div>
            ))}
            {requestWindow && (
                <RequestModal
                    userId={user?.id}
                    tournamentId={selectedTournament.id}
                    token={token}
                    isOpen={requestWindow}
                    onClose={closeRequestModal}
                />
            )}
        </>
    );
};
