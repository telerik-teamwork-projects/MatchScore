import "./playerSearchModal.scss";
import { Link } from "react-router-dom";
import { PLAYERS } from "../../../routes/routes";
import { BASE_PATH } from "../../../routes/paths";

export const PlayerSearchModal = ({ searchResults, onClose }) => {
    return (
        <div className="player-search-results-modal">
            <div className="modalContent">
                <h2>Players Search</h2>
                <ul>
                    {searchResults?.map((player) => (
                        <li key={player.id}>
                            <div className="modalplayerInfo">
                                <div className="modalplayerInfoLeft">
                                    <div className="modalplayerData">
                                        {player.profile_img ? (
                                            <img
                                                src={`${BASE_PATH}${player.profile_img}`}
                                                alt={player.full_name}
                                                className="modalplayerImage"
                                            />
                                        ) : (
                                            <img
                                                src="/images/avatar/default.jpg"
                                                alt={player.full_name}
                                                className="modalplayerImage"
                                            />
                                        )}
                                    </div>
                                    <span className="modalplayerplayername">
                                        {player.full_name}
                                    </span>
                                </div>
                                <div className="modalplayerInfoRight">
                                    <Link
                                        to={`${PLAYERS}/${player.id}`}
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
