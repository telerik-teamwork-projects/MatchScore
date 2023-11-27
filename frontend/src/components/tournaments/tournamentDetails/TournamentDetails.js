import "./tournamentDetails.scss";

import { useContext, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getOne } from "../../../services/tournamentService";
import { TournamentKnockoutTree } from "../tournamentKnockoutTree/TournamentKnockoutTree";
import { TournamentLeagueTree } from "../tournamentLeagueTree/TournamentLeagueTree";
import { PROFILE } from "../../../routes/routes";
import { TournamentRequest } from "../tournamentRequests/TournamentRequest";
import { AuthContext } from "../../../contexts/authContext";
import { getTournamentRequests } from "../../../services/requestService";
import { StartDateModal } from "../../startDateModal/StartDateModal";
import { EditStartDate } from "../../editStartDate/EditStartDate";
import { EditTournamentPlayers } from "../../editTournamentPlayers/EditTournamentPlayers";

export const TournamentDetails = () => {
    const { tournamentId } = useParams();
    const { token, user } = useContext(AuthContext);
    const [tournament, setTournament] = useState(null);

    const [requestModalOpen, setRequestModalOpen] = useState(false);
    const [requestsResult, setRequestsResult] = useState(null);

    const [startModalOpen, setStartModalOpen] = useState(false);

    const [editPlayersOpen, setEditPlayersOpen] = useState(false);
    const [editDateOpen, setEditDateOpen] = useState(false);

    const closeRequestModal = () => {
        setRequestModalOpen(false);
    };

    const onRequests = async (e) => {
        e.preventDefault();

        try {
            const requestsData = await getTournamentRequests(
                tournamentId,
                token
            );
            setRequestsResult(requestsData);
            setRequestModalOpen(true);
        } catch (error) {
            console.error(error);
        }
    };

    const openEditPlayersModal = () => {
        setEditPlayersOpen(true);
    };

    const openStartModal = () => {
        setStartModalOpen(true);
    };

    const openEditDate = () => {
        setEditDateOpen(true);
    };

    useEffect(() => {
        try {
            const fetchData = async () => {
                const tournamentData = await getOne(tournamentId);
                setTournament(tournamentData);
            };
            fetchData();
        } catch (error) {
            console.error(error);
        }
    }, [tournamentId]);

    return (
        <div className="tournamentDetails">
            <h1 className="tournamentTitle">{tournament?.title}</h1>
            <p className="tournamentDesc">
                {tournament?.description
                    ? tournament?.description
                    : "No description"}
            </p>
            <div className="tournamentData">
                <div className="tournamentOwner">
                    <p>Owner:</p>
                    <Link
                        className="link"
                        to={`${PROFILE}/${tournament?.owner.id}`}
                    >
                        {tournament?.owner.username}
                    </Link>
                </div>
                <div className="tournamentStatus">
                    <p>Status:</p>
                    <span>{tournament?.status}</span>
                </div>
                <div className="tournamentFormat">
                    <p>Type of Tournament:</p>
                    <span>{tournament?.format}</span>
                </div>
                <div className="tournamentMatchFormat">
                    <p>Match Format:</p>
                    <span>{tournament?.match_format}</span>
                </div>
                <div className="tournamentRounds">
                    <p>Rounds:</p>
                    <span>{tournament?.rounds}</span>
                </div>
                <div className="tournamentThirdPlace">
                    <p>Third Place Award:</p>
                    <span>{tournament?.third_place ? "Yes" : "No"}</span>
                </div>

                <div className="tournamentLocation">
                    <p>Location:</p>
                    <span>{tournament?.location}</span>
                </div>
                <div className="tournamentDates">
                    <p>Date:</p>
                    <span>
                        {tournament?.start_date.slice(0, 10)} -{" "}
                        {tournament?.end_date &&
                            tournament?.end_date.slice(0, 10)}
                    </span>
                </div>
                {(user?.id === tournament?.owner.id ||
                    user?.role === "admin") && (
                    <div className="requestsBtns">
                        <button
                            className="openRequestsBtn"
                            type="button"
                            onClick={(e) => onRequests(e)}
                        >
                            Show Requests
                        </button>
                        <button
                            onClick={openStartModal}
                            className="startTournamentBtn"
                            type="button"
                        >
                            Start Tournament
                        </button>
                        <button
                            className="editPlayersBtn"
                            type="button"
                            onClick={openEditPlayersModal}
                        >
                            Edit Players
                        </button>
                        <button
                            className="editDateBtn"
                            type="button"
                            onClick={openEditDate}
                        >
                            Edit Start Date
                        </button>
                    </div>
                )}
            </div>

            {tournament?.format === "knockout" && (
                <div>
                    <TournamentKnockoutTree
                        tournamentId={tournament?.id}
                        token={token}
                    />
                </div>
            )}
            {tournament?.format === "league" && (
                <div>
                    <TournamentLeagueTree
                        tournamentId={tournament?.id}
                        token={token}
                    />
                </div>
            )}

            {requestModalOpen && (
                <TournamentRequest
                    requests={requestsResult}
                    setRequests={setRequestsResult}
                    onClose={closeRequestModal}
                    token={token}
                />
            )}

            {startModalOpen && (
                <StartDateModal
                    tournamentId={tournamentId}
                    token={token}
                    onClose={() => setStartModalOpen(false)}
                />
            )}

            {editDateOpen && (
                <EditStartDate
                    tournamentId={tournamentId}
                    token={token}
                    onClose={() => setEditDateOpen(false)}
                />
            )}

            {editPlayersOpen && (
                <EditTournamentPlayers
                    tournamentId={tournamentId}
                    token={token}
                    onClose={() => setEditPlayersOpen(false)}
                />
            )}
        </div>
    );
};
