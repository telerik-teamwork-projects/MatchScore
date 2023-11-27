import "./startDateModal.scss";
import { useState } from "react";
import { startKnockoutTournament } from "../../services/tournamentService";

export const StartDateModal = ({ tournamentId, token, onClose }) => {
    const [formData, setFormData] = useState({
        start_date: "",
    });

    const onChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const onTournamentStart = async (e) => {
        e.preventDefault();
        const formattedStartDate = `${formData.start_date}T00:00:00`;

        try {
            await startKnockoutTournament(tournamentId, token, {
                date: formattedStartDate,
            });
            window.location.reload();
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="startDateModal">
            <form
                className="startDateContainer"
                onSubmit={(e) => onTournamentStart(e)}
            >
                <h3>Select Date</h3>
                <input
                    placeholder="Start Date"
                    className="startDateInput"
                    type="date"
                    name="start_date"
                    value={formData.start_date}
                    onChange={(e) => onChange(e)}
                    required
                />
                <div className="startDateBtns">
                    <button className="submitBtn" type="submit">
                        Start Tournament
                    </button>
                    <button
                        className="closeBtn"
                        type="button"
                        onClick={onClose}
                    >
                        Close
                    </button>
                </div>
            </form>
        </div>
    );
};
