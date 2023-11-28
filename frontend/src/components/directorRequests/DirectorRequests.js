import "./directorRequests.scss";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { PROFILE } from "../../routes/routes";
import {
    acceptDirectorRequest,
    rejectDirectorRequest,
} from "../../services/requestService";
import { ErrorMessage } from "../responseMessages/errorMessages/ErrorMessages";
import { SuccessMessage } from "../responseMessages/successMessages/SuccessMessages";
import { FadeLoader } from "react-spinners";

export const DirectorRequests = ({ requests, setRequests, onClose, token }) => {
    const [success, setSuccess] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setTimeout(() => {
            setLoading(false);
        }, 500);
    }, []);

    const onAccept = async (requestId) => {
        try {
            const result = await acceptDirectorRequest(requestId, token);
            setError(null);
            setSuccess(result);
            updateStatus(requestId, "accepted");
        } catch (error) {
            setError(error.response.data.detail);
            setSuccess(null);
        }
    };

    const onReject = async (requestId) => {
        try {
            await rejectDirectorRequest(requestId, token);
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
        <div className="directorRequests">
            <div className="directorRequestsWrapper">
                <h2>Director Requests</h2>
                {loading ? (
                    <div className="spinner-container">
                        <FadeLoader color="darkgray" loading={true} />
                    </div>
                ) : (
                    <ul>
                        {requests?.map((request) => (
                            <li key={request.id}>
                                <div>
                                    <strong>Email:</strong>{" "}
                                    <Link
                                        className="link"
                                        onClick={onClose}
                                        to={`${PROFILE}/${request.user_id}`}
                                    >
                                        {request.email}
                                    </Link>
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
                                                    onReject(request.id);
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
                )}
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
