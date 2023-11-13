import "./createTournamentModal.scss";
import { useState } from "react";

import { create } from "../../../services/tournamentService";
import { ErrorMessage } from "../../responseMessages/errorMessages/ErrorMessages";

export const CreateTournamentModal = ({
    user,
    token,
    setTournaments,
    onClose,
}) => {
    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        format: "",
        title: "",
        description: "",
        match_format: "",
        rounds: "",
        third_place: false,
        status: "",
        location: "",
        start_date: "",
        end_date: "",
    });

    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async (e) => {
        e.preventDefault();

        try {
            const formDataWithUserId = {
                ...formData,
                owner_id: user?.id,
            };

            const result = await create(formDataWithUserId, token);
            setTournaments((prevTournaments) => [result, ...prevTournaments]);
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
                                placeholder="Rounds"
                                type="number"
                                name="rounds"
                                value={formData.rounds}
                                onChange={(e) => onChange(e)}
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
                                name="format"
                                value={formData.format}
                                onChange={(e) => onChange(e)}
                            >
                                <option value="" disabled>
                                    Select Tournament Format
                                </option>
                                <option value="knockout">Knockout</option>
                                <option value="league">League</option>
                            </select>
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
                            <select
                                className="createSelect"
                                name="status"
                                value={formData.status}
                                onChange={(e) => onChange(e)}
                            >
                                <option value="" disabled>
                                    Select Status
                                </option>
                                <option value="open">Open</option>
                                <option value="closed">Closed</option>
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

                                    <label
                                        className="dateInputLabel"
                                        htmlFor="end_date"
                                    >
                                        {formData.end_date
                                            ? "End Date"
                                            : "Select End Date"}
                                        <input
                                            className="createInput dateInput"
                                            type="date"
                                            id="end_date"
                                            name="end_date"
                                            value={formData.end_date}
                                            onChange={(e) => onChange(e)}
                                        />
                                    </label>
                                </div>
                                <input
                                    type="checkbox"
                                    name="third_place"
                                    checked={formData.third_place}
                                    onChange={(e) =>
                                        setFormData({
                                            ...formData,
                                            third_place: e.target.checked,
                                        })
                                    }
                                />
                                Include Third Place
                            </label>
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
        </div>
    );
};
