import "./userSearchModal.scss";
import { useEffect } from "react";
import { Link } from "react-router-dom";
import { PROFILE } from "../../../routes/routes";
import { BASE_PATH } from "../../../routes/paths";
import { FadeLoader } from "react-spinners";
import { useState } from "react";

export const UserSearchModal = ({ searchResults, onClose }) => {
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setTimeout(() => {
            setLoading(false);
        }, 500);
    }, []);

    return (
        <div className="user-search-results-modal">
            <div className="modalContent">
                <h2>Users Search</h2>
                {loading ? (
                    <div className="spinner-container">
                        <FadeLoader color="darkgray" loading={true} />
                    </div>
                ) : (
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
                )}
                <div className="modalBtn">
                    <button onClick={onClose}>Close</button>
                </div>
            </div>
        </div>
    );
};
