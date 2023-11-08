import { Link } from "react-router-dom";
import "./userSearchModal.scss";
import { PROFILE } from "../../routes/routes";
import { USER_BASE_PATH } from "../../routes/paths";

export const UserSearchModal = ({ users, onClose }) => {
    return (
        <div className="user-search-results-modal">
            <div className="modalContent">
                <h2>Search Results</h2>
                <ul>
                    {users.map((user) => (
                        <li key={user.id}>
                            <div className="modalUserInfo">
                                <div className="modalUserInfoLeft">
                                    <div className="modalUserData">
                                        {user.profile_img ? (
                                            <img
                                                src={`${USER_BASE_PATH}${user.profile_img}`}
                                                alt={user.full_name}
                                                className="modalUserImage"
                                            />
                                        ) : (
                                            <img
                                                src="/images/teams/liverpool.png"
                                                alt={user.username}
                                                className="modalUserImage"
                                            />
                                        )}
                                    </div>
                                    <span className="modalUserUsername">
                                        {user?.username}
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
