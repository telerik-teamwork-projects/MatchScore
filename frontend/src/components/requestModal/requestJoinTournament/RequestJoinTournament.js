import "./requestJoinTournament.scss";
import { useState } from "react";
import { ErrorMessage } from "../../responseMessages/errorMessages/ErrorMessages";
import { SuccessMessage } from "../../responseMessages/successMessages/SuccessMessages";
import {
    sendTournamentRequestNoPlayer,
    sendTournamentRequestWithPlayer,
} from "../../../services/requestService";

export const RequestJoinTournament = ({ tournamentId, token, onClose }) => {
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

    const handleSubmitNoPlayer = async () => {
        try {
            const result = await sendTournamentRequestNoPlayer(
                tournamentId,
                token,
                formData
            );
            setFormData({
                full_name: "",
                country: "",
                sports_club: "",
            });
            setError(null);
            setSuccessMsg(result);
        } catch (error) {
            setFormData({
                full_name: "",
                country: "",
                sports_club: "",
            });
            setSuccessMsg(null);
            setError(error.response.data.detail);
        }
    };

    const handleSubmitWithPlayer = async () => {
        try {
            const result = await sendTournamentRequestWithPlayer(
                tournamentId,
                token,
                formData
            );
            setFormData({
                full_name: "",
                country: "",
                sports_club: "",
            });
            setError(null);
            setSuccessMsg(result);
        } catch (error) {
            setFormData({
                full_name: "",
                country: "",
                sports_club: "",
            });
            setSuccessMsg(null);
            setError(error.response.data.detail);
        }
    };

    return (
        <div className="requestModal">
            <div className="requestContent">
                <h2>Join Tournament Request</h2>
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
                    <div className="requestBtns">
                        <button
                            className="requestSubmit"
                            type="button"
                            onClick={handleSubmitNoPlayer}
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
                    <h3>Already have a player profile ?</h3>
                    <button
                        className="submitExistingPlayer"
                        type="button"
                        onClick={handleSubmitWithPlayer}
                    >
                        Submit as a Player
                    </button>
                </form>
            </div>
        </div>
    );
};
