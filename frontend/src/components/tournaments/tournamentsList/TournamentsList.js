import "./tournamentList.scss";

import { PROFILE, TOURNAMENTS } from "../../../routes/routes";
import { Link } from "react-router-dom";
import { BASE_PATH } from "../../../routes/paths";
import { useState } from "react";
import { RequestJoinTournament } from "../../requestModal/requestJoinTournament/RequestJoinTournament";
import { Pagination } from "../../pagination/Pagination";
import { FadeLoader } from "react-spinners";

export const TournamentsList = ({
    user,
    token,
    handlePageChange,
    tournamentsData,
    loading,
}) => {
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
            {loading ? (
                <div className="spinner-container">
                    <FadeLoader color="darkgray" loading={true} />
                </div>
            ) : (
                tournamentsData?.tournaments.map((tournament) => (
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
                                                src={`${BASE_PATH}${tournament.owner.profile_img}`}
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
                                <div className="tournamentFormat">
                                    <p>Format:</p>
                                    <span>{tournament.format}</span>
                                </div>
                                <div className="tournamentStatus">
                                    <p>Status:</p>
                                    <span>{tournament.status}</span>
                                </div>
                                <div className="tournamentDate">
                                    <p>Date:</p>
                                    <span>
                                        {tournament.start_date &&
                                            tournament.start_date.slice(
                                                0,
                                                10
                                            )}{" "}
                                        -{" "}
                                        {tournament.end_date &&
                                            tournament.end_date.slice(0, 10)}
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
                ))
            )}
            {tournamentsData && (
                <Pagination
                    handlePageChange={handlePageChange}
                    dataToFetch={tournamentsData}
                />
            )}
            {requestWindow && (
                <RequestJoinTournament
                    userId={user?.id}
                    tournamentId={selectedTournament.id}
                    token={token}
                    onClose={closeRequestModal}
                />
            )}
        </>
    );
};
