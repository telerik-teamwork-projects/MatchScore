import "./tournamentsSearchModal.scss";
import { Link } from "react-router-dom";
import { TOURNAMENTS } from "../../../routes/routes";

export const TournamentSearchModal = ({ searchResults, onClose }) => {
    return (
        <div className="user-search-results-modal">
            <div className="modalContent">
                <h2>Tournaments Search</h2>
                <ul>
                    {searchResults?.map((tournament) => (
                        <li key={tournament.id}>
                            <div className="modalUserInfo">
                                <div className="modalUserInfoLeft">
                                    <span className="modalUserUsername">
                                        {tournament.title}
                                    </span>
                                </div>
                                <div className="modalUserInfoRight">
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
                <div className="modalBtn">
                    <button onClick={onClose}>Close</button>
                </div>
            </div>
        </div>
    );
};
