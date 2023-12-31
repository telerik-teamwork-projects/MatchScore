import "./requestBecomePlayer.scss";
import { useState } from "react";
import { ErrorMessage } from "../../responseMessages/errorMessages/ErrorMessages";
import { SuccessMessage } from "../../responseMessages/successMessages/SuccessMessages";
import { sendPlayerRequest } from "../../../services/requestService";

export const RequestBecomePlayer = ({ userId, token, onClose }) => {
    const [error, setError] = useState(null);
    const [successMsg, setSuccessMsg] = useState(null);
    const [formData, setFormData] = useState({
        full_name: "",
        country: "",
        sports_club: "",
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async () => {
        try {
            const result = await sendPlayerRequest(userId, token, formData);
            formData.full_name = "";
            formData.country = "";
            formData.sports_club = "";
            setError(null);
            setSuccessMsg(result);
        } catch (error) {
            formData.full_name = "";
            formData.country = "";
            formData.sports_club = "";
            setSuccessMsg(null);
            setError(error.response.data.detail);
        }
    };

    return (
        <div className="requestPlayerModal">
            <div className="requestPlayerContent">
                <h2>Ask to become a player</h2>
                <form>
                    <input
                        type="text"
                        name="full_name"
                        placeholder="Full Name"
                        value={formData.full_name}
                        onChange={handleChange}
                        autoComplete="text"
                    />
                    <input
                        type="text"
                        name="country"
                        placeholder="Country"
                        value={formData.country}
                        onChange={handleChange}
                        autoComplete="text"
                    />
                    <input
                        type="text"
                        name="sports_club"
                        placeholder="Sports Club"
                        value={formData.sports_club}
                        onChange={handleChange}
                        autoComplete="text"
                    />

                    {error && <ErrorMessage message={error} />}
                    {successMsg && <SuccessMessage message={successMsg} />}
                    <div className="requestPlayerBtns">
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
                </form>
            </div>
        </div>
    );
};
