import "./tournamentRequest.scss";
import { PROFILE } from "../../../routes/routes";
import { Link } from "react-router-dom";
import {
    acceptTournamentRequest,
    rejectTournamentRequest,
} from "../../../services/tournamentService";
import { useState } from "react";
import { ErrorMessage } from "../../responseMessages/errorMessages/ErrorMessages";
import { SuccessMessage } from "../../responseMessages/successMessages/SuccessMessages";

export const TournamentRequest = ({
    requests,
    setRequests,
    onClose,
    token,
}) => {
    const [success, setSuccess] = useState(null);
    const [error, setError] = useState(null);

    const onAccept = async (requestId) => {
        try {
            await acceptTournamentRequest(requestId, token);
            setError(null);
            setSuccess("User accepted");
            updateStatus(requestId, "accepted");
        } catch (error) {
            setError(error.response.data.detail);
            setSuccess(null);
        }
    };

    const onReject = async (requestId) => {
        try {
            await rejectTournamentRequest(requestId, token);
            setError(null);
            setSuccess("User rejected");
            updateStatus(requestId, "rejected");
        } catch (error) {
            setError(error.response.data.detail);
            setSuccess(null);
        }
    };

    const updateStatus = (requestId, status) => {
        const updatedRequests = requests.map((request) =>
            request.id === requestId ? { ...request, status } : request
        );
        setRequests(updatedRequests);
    };

    return (
        <div className="tournamentRequests">
            <div className="tournamentRequestsWrapper">
                <h2>Tournament Requests</h2>
                <ul>
                    {requests.map((request) => (
                        <li key={request.id}>
                            <div>
                                <strong>Full Name:</strong>{" "}
                                <Link
                                    className="link"
                                    to={`${PROFILE}/${request.user_id}`}
                                >
                                    {request.full_name}
                                </Link>
                            </div>
                            <div>
                                <strong>Country:</strong>{" "}
                                {request.country || "N/A"}
                            </div>
                            <div>
                                <strong>Sports Club:</strong>{" "}
                                {request.sports_club || "N/A"}
                            </div>
                            <div>
                                <strong>Status:</strong> {request.status}
                            </div>
                            {request.status === "pending" && (
                                <>
                                    <hr />
                                    <div className="requestBtns">
                                        <button
                                            className="requestAccept"
                                            onClick={() => {
                                                onAccept(request.id);
                                            }}
                                        >
                                            Accept
                                        </button>
                                        <button
                                            className="requestReject"
                                            onClick={() => {
                                                onReject(
                                                    request.id,
                                                    request.player_id,
                                                    request.tournament_id
                                                );
                                            }}
                                        >
                                            Reject
                                        </button>
                                    </div>
                                </>
                            )}
                        </li>
                    ))}
                </ul>
                {error ? (
                    <ErrorMessage message={error} />
                ) : (
                    <SuccessMessage message={success} />
                )}
                <div className="modalBtn">
                    <button onClick={onClose}>Close</button>
                </div>
            </div>
        </div>
    );
};
