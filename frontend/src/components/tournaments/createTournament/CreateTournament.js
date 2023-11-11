import "./createTournament.scss";
import { useState } from "react";

import { create } from "../../../services/tournamentService";
import { AuthErrorMessage } from "../../errorMessages/authErrorMessages";
import { TOURNAMENTS } from "../../../routes/routes";

export const CreateTournament = ({ user, token, setTournaments }) => {
    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        format: "",
        title: "",
        match_format: "",
        rounds: "",
        third_place: false,
        status: "",
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
            setFormData({
                format: "",
                title: "",
                match_format: "",
                rounds: "",
                third_place: false,
                status: "",
                start_date: "",
                end_date: "",
            });
        } catch (error) {
            setError(error.response.data.detail);
        }
    };

    return (
        <>
            {(user?.role === "admin" || user?.role === "director") && (
                <form
                    className="createContainer"
                    method="post"
                    onSubmit={(e) => onSubmit(e)}
                >
                    <div className="createWrapper">
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
                        {error && <AuthErrorMessage message={error} />}
                        <hr className="createHr" />
                        <div className="createBottom">
                            <button className="createButton">Create</button>
                        </div>
                    </div>
                </form>
            )}
        </>
    );
};
