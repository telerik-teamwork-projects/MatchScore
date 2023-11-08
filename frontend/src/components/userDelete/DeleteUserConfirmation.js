import "./deleteUserConfirmatio.scss"


export const DeleteUserConfirmation = ({ isOpen, onConfirm, onCancel }) => {
    return (
        <div className={`delete-confirmation ${isOpen ? "show" : ""}`}>
            <div className="confirmation-content">
                <p>Are you sure you want to delete this user?</p>
                <button onClick={onConfirm}>Yes</button>
                <button onClick={onCancel}>No</button>
            </div>
        </div>
    );
};
