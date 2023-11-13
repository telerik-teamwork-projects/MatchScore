import "./tournamentDetails.scss";

import { useContext, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getOne } from "../../../services/tournamentService";
import { TournamentTree } from "../tournamentTree/TournamentTree";
import { PROFILE } from "../../../routes/routes";
import { TournamentRequest } from "../tournamentRequests/TournamentRequest";
import { AuthContext } from "../../../contexts/authContext";
import { getRequests } from "../../../services/tournamentService";

export const TournamentDetails = () => {
    const { tournamentId } = useParams();
    const { token } = useContext(AuthContext);
    const [tournament, setTournament] = useState(null);

    const [requestModalOpen, setRequestModalOpen] = useState(false);
    const [requestsResult, setRequestsResult] = useState(null);

    const closeRequestModal = () => {
        setRequestModalOpen(false);
    };

    const onRequests = async (e) => {
        e.preventDefault();

        try {
            const requestsData = await getRequests(tournamentId, token);
            setRequestsResult(requestsData);
            setRequestModalOpen(true);
        } catch (error) {
            console.error(error);
        }
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
                        {tournament?.end_date.slice(0, 10)}
                    </span>
                </div>
                <div className="requestsBtns">
                    <button
                        className="openRequestsbtn"
                        type="button"
                        onClick={(e) => onRequests(e)}
                    >
                        Show Requests
                    </button>
                </div>
            </div>
            <div>
                <TournamentTree tournament={tournament} />
            </div>
            {requestModalOpen && (
                <TournamentRequest
                    requests={requestsResult}
                    onClose={closeRequestModal}
                />
            )}
        </div>
    );
};
