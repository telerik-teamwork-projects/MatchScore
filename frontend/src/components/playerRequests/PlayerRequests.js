import "./playerRequests.scss";
import { useState } from "react";
import { Link } from "react-router-dom";
import { PROFILE } from "../../routes/routes";
import { acceptPlayerRequest } from "../../services/playerService";
import { ErrorMessage } from "../responseMessages/errorMessages/ErrorMessages";
import { SuccessMessage } from "../responseMessages/successMessages/SuccessMessages";

export const PlayerRequests = ({ requests, onClose, token }) => {
    const [success, setSuccess] = useState(null);
    const [error, setError] = useState(null);

    const onAccept = async (requestId) => {
        try {
            await acceptPlayerRequest(requestId, token);
            setError(null);
            setSuccess("User accepted");
        } catch (error) {
            setError(error.response.data.detail);
            setSuccess(null);
        }
    };

    return (
        <div className="playerRequests">
            <div className="playerRequestsWrapper">
                <h2>Notifications</h2>
                <ul>
                    {requests?.map((request) => (
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
                                        <button className="requestReject">
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
