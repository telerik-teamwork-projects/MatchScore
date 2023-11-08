import "./userSearchModal.scss";

export const UserSearchModal = ({ users, onClose }) => {
    return (
        <div className="user-search-results-modal">
            <div className="modalContent">
                <h2>Search Results</h2>
                <ul>
                    {users.map((user) => (
                        <li key={user.id}>
                            <div className="modalUserInfo">
                                <span>{user.username}</span>
                                <span>{user.email}</span>
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
