import "./requestLinkWithPlayer.scss";
import { useState } from "react";
import { ErrorMessage } from "../responseMessages/errorMessages/ErrorMessages";
import { SuccessMessage } from "../responseMessages/successMessages/SuccessMessages";
import { sendLinkToPlayerRequest } from "../../services/requestService";

export const RequestLinkWithPlayer = ({ token, onClose }) => {
    const [error, setError] = useState(null);
    const [successMsg, setSuccessMsg] = useState(null);
    const [formData, setFormData] = useState({
        full_name: "",
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async () => {
        try {
            const result = await sendLinkToPlayerRequest(token, formData);
            formData.full_name = "";
            setError(null);
            setSuccessMsg(result);
        } catch (error) {
            setSuccessMsg(null);
            setError(error.response.data.detail);
        }
    };

    return (
        <div className="requestLinkToPlayerModal">
            <div className="requestLinkToPlayerContent">
                <h2>Link with an existing player</h2>
                <form>
                    <input
                        type="text"
                        name="full_name"
                        placeholder="Enter player's full name"
                        value={formData.full_name}
                        onChange={handleChange}
                        autoComplete="text"
                    />
                </form>
                {error && <ErrorMessage message={error} />}
                {successMsg && <SuccessMessage message={successMsg} />}
                <div className="requestLinkToPlayerBtns">
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
