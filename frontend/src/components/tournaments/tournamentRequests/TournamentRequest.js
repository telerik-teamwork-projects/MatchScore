import "./tournamentRequest.scss";

export const TournamentRequest = ({ requests, onClose }) => {
    return (
        <div className="tournamentRequests">
            <div className="tournamentRequestsWrapper">
                <h2>Tournament Requests</h2>
                <ul>
                    {requests.map((request) => (
                        <li key={request.id}>
                            <div>
                                <strong>Full Name:</strong> {request.full_name}
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
                                <button className="requestAccept">
                                    Accept
                                </button>
                                <button className="requestReject">
                                    Reject
                                </button>
                            </div>
                        </li>
                    ))}
                </ul>
                <div className="modalBtn">
                    <button onClick={onClose}>Close</button>
                </div>
            </div>
        </div>
    );
};
