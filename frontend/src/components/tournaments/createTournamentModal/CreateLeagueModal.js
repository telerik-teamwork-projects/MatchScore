import "./createTournamentModal.scss";
import { useState } from "react";

import { createLeague } from "../../../services/tournamentService";
import { ErrorMessage } from "../../responseMessages/errorMessages/ErrorMessages";
import { ParticipantSelection } from "../../participantSelection/ParticipantSelection";

export const CreateLeagueModal = ({ user, token, onClose }) => {
    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        match_format: "",
        location: "",
        start_date: "",
        participants: [],
    });

    const [showParticipantSelection, setShowParticipantSelection] =
        useState(false);

    const handlePlayerSelection = (selectedPlayers, newPlayerDetails) => {
        const updatedParticipants = [
            ...formData.participants,
            ...selectedPlayers,
        ];

        if (newPlayerDetails) {
            updatedParticipants.push(newPlayerDetails);
        }

        setFormData({ ...formData, participants: updatedParticipants });
        setShowParticipantSelection(false);
    };

    const openParticipantSelection = () => {
        setShowParticipantSelection(true);
    };
    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async (e) => {
        e.preventDefault();
        const formattedStartDate = `${formData.start_date}T00:00:00`;

        try {
            const formDataWithUserId = {
                ...formData,
                start_date: formattedStartDate,
                owner_id: user?.id,
            };

            await createLeague(formDataWithUserId, token);
            onClose();
        } catch (error) {
            setError(error.response.data.detail);
        }
    };

    return (
        <div className="createModal">
            {(user?.role === "admin" || user?.role === "director") && (
                <form
                    className="createFormContainer"
                    method="post"
                    onSubmit={(e) => onSubmit(e)}
                >
                    <div className="createFormWrapper">
                        <div className="createTop">
                            <h1>Create Tournament</h1>

                            <input
                                className="createInput"
                                placeholder="Title"
                                type="text"
                                name="title"
                                value={formData.title}
                                onChange={(e) => onChange(e)}
                                autoComplete="text"
                            />

                            <input
                                className="createInput"
                                placeholder="Location"
                                type="text"
                                name="location"
                                value={formData.location}
                                onChange={(e) => onChange(e)}
                                autoComplete="text"
                            />

                            <textarea
                                className="createInput"
                                placeholder="Short Description"
                                name="description"
                                value={formData.description}
                                onChange={(e) => onChange(e)}
                            />
                            <select
                                className="createSelect"
                                name="match_format"
                                value={formData.match_format}
                                onChange={(e) => onChange(e)}
                            >
                                <option value="" disabled>
                                    Select Match Format
                                </option>
                                <option value="time">Time</option>
                                <option value="score">Score</option>
                            </select>
                            <label>
                                <div className="dateInputContainer">
                                    <label
                                        className="dateInputLabel"
                                        htmlFor="start_date"
                                    >
                                        {formData.start_date
                                            ? "Start Date"
                                            : "Select Start Date"}
                                        <input
                                            className="createInput dateInput"
                                            type="date"
                                            id="start_date"
                                            name="start_date"
                                            value={formData.start_date}
                                            onChange={(e) => onChange(e)}
                                        />
                                    </label>
                                </div>
                            </label>
                            <button
                                className="participantsSelection"
                                type="button"
                                onClick={openParticipantSelection}
                            >
                                Select Participants
                            </button>
                        </div>
                        {error && <ErrorMessage message={error} />}
                        <hr className="createHr" />
                        <div className="createBottom">
                            <button className="createButton">Create</button>
                            <button
                                className="closeButton"
                                type="button"
                                onClick={onClose}
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                </form>
            )}
            {showParticipantSelection && (
                <ParticipantSelection
                    selectedPlayers={formData.participants}
                    onPlayerSelection={handlePlayerSelection}
                    onClose={() => setShowParticipantSelection(false)}
                />
            )}
        </div>
    );
};
