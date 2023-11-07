import "./logoutConfirmation.scss"


export const LogoutConfirmation = ({ isOpen, onConfirm, onCancel }) => {
    return (
        <div className={`logout-confirmation ${isOpen ? "show" : ""}`}>
            <div className="confirmation-content">
                <p>Are you sure you want to log out?</p>
                <button onClick={onConfirm}>Yes</button>
                <button onClick={onCancel}>No</button>
            </div>
        </div>
    );
};
