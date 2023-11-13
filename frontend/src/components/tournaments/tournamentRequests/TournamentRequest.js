import "./tournamentRequest.scss";
import { PROFILE } from "../../../routes/routes";
import { Link } from "react-router-dom";
import { acceptRequest } from "../../../services/tournamentService";
import { useState } from "react";
import { ErrorMessage } from "../../responseMessages/errorMessages/ErrorMessages";
import { SuccessMessage } from "../../responseMessages/successMessages/SuccessMessages";

export const TournamentRequest = ({ requests, onClose, token }) => {
    const [success, setSuccess] = useState(null);
    const [error, setError] = useState(null);

    const onAccept = async (userId, tournamentId) => {
        try {
            await acceptRequest(userId, tournamentId, token);
            setError(null);
            setSuccess("User accepted");
        } catch (error) {
            setError(error.response.data.detail);
            setSuccess(null);
        }
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
                            <hr />
                            <div className="requestBtns">
                                <button
                                    className="requestAccept"
                                    onClick={() => {
                                        onAccept(
                                            request.user_id,
                                            request.tournament_id
                                        );
                                    }}
                                >
                                    Accept
                                </button>
                                <button className="requestReject">
                                    Reject
                                </button>
                            </div>
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
