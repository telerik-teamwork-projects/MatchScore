import "./tournamentsSearchModal.scss";
import { useEffect } from "react";
import { Link } from "react-router-dom";
import { TOURNAMENTS } from "../../../routes/routes";
import { useState } from "react";
import { FadeLoader } from "react-spinners";

export const TournamentSearchModal = ({ searchResults, onClose }) => {
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        setTimeout(() => {
            setLoading(false);
        }, 500);
    }, []);

    return (
        <div className="tournament-search-results-modal">
            <div className="modalContent">
                <h2>Tournaments Search</h2>
                {loading ? (
                    <div className="spinner-container">
                        <FadeLoader color="darkgray" loading={true} />
                    </div>
                ) : (
                    <ul>
                        {searchResults?.map((tournament) => (
                            <li key={tournament.id}>
                                <div className="modaltournamentInfo">
                                    <div className="modaltournamentInfoLeft">
                                        <span className="modaltournamenttournamentname">
                                            {tournament.title}
                                        </span>
                                    </div>
                                    <div className="modaltournamentInfoRight">
                                        <Link
                                            to={`${TOURNAMENTS}/${tournament.id}`}
                                            onClick={onClose}
                                        >
                                            View
                                        </Link>
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
                <div className="modalBtn">
                    <button onClick={onClose}>Close</button>
                </div>
            </div>
        </div>
    );
};
