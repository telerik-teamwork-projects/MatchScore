import { useState } from "react";
import "./requestModal.scss";
export const RequestModal = ({ isOpen, onClose, onSubmit }) => {
    const [formData, setFormData] = useState({
        full_name: "",
        country: "",
        sports_club: "",
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = () => {
        onSubmit(formData);
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
                    />
                    <input
                        type="text"
                        name="country"
                        placeholder="Country"
                        value={formData.country}
                        onChange={handleChange}
                    />
                    <input
                        type="text"
                        name="sports_club"
                        placeholder="Sports Club"
                        value={formData.sports_club}
                        onChange={handleChange}
                    />
                    <div className="requestBtns">
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
