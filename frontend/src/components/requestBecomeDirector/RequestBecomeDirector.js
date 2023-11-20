import "./requestBecomeDirector.scss";
import { useState } from "react";
import { ErrorMessage } from "../responseMessages/errorMessages/ErrorMessages";
import { SuccessMessage } from "../responseMessages/successMessages/SuccessMessages";
import { sendDirectorRequest } from "../../services/requestService";

export const RequestBecomeDirector = ({ user, token, onClose }) => {
    const [error, setError] = useState(null);
    const [successMsg, setSuccessMsg] = useState(null);

    const handleSubmit = async () => {
        try {
            const result = await sendDirectorRequest(
                user?.id,
                user?.email,
                token
            );
            setError(null);
            setSuccessMsg(result);
        } catch (error) {
            setSuccessMsg(null);
            setError(error.response.data.detail);
        }
    };

    return (
        <div className="requestDirectorModal">
            <div className="requestDirectorContent">
                <h2>Confirm sending a director request</h2>

                {error && <ErrorMessage message={error} />}
                {successMsg && <SuccessMessage message={successMsg} />}
                <div className="requestDirectorBtns">
                    <button
                        className="requestSubmit"
                        type="button"
                        onClick={handleSubmit}
                    >
                        Submit
                    </button>
                    <button
                        className="requestClose"
                        type="button"
                        onClick={() => onClose()}
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};
