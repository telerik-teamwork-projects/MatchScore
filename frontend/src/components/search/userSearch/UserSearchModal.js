import "./userSearchModal.scss";
import { Link } from "react-router-dom";
import { PROFILE } from "../../../routes/routes";
import { BASE_PATH } from "../../../routes/paths";

export const UserSearchModal = ({ searchResults, onClose }) => {
    return (
        <div className="user-search-results-modal">
            <div className="modalContent">
                <h2>Users Search</h2>
                <ul>
                    {searchResults?.map((user) => (
                        <li key={user.id}>
                            <div className="modalUserInfo">
                                <div className="modalUserInfoLeft">
                                    <div className="modalUserData">
                                        {user.profile_img ? (
                                            <img
                                                src={`${BASE_PATH}${user.profile_img}`}
                                                alt={user.full_name}
                                                className="modalUserImage"
                                            />
                                        ) : (
                                            <img
                                                src="/images/avatar/default.jpg"
                                                alt={user.username}
                                                className="modalUserImage"
                                            />
                                        )}
                                    </div>
                                    <span className="modalUserUsername">
                                        {user.username}
                                    </span>
                                </div>
                                <div className="modalUserInfoRight">
                                    <Link
                                        to={`${PROFILE}/${user.id}`}
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
