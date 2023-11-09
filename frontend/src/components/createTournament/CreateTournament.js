import "./createTournament.scss";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export const CreateTournament = ({ user, token }) => {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        format: "",
        title: "",
        match_format: "",
        rounds: 0,
        third_place: false,
    });

    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async (e) => {
        e.preventDefault();

        return "";
    };

    return (
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
                        placeholder="Format"
                        type="text"
                        name="format"
                        value={formData.format}
                        onChange={(e) => onChange(e)}
                        autoComplete="text"
                    />
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
                        placeholder="Match Format"
                        type="text"
                        name="match_format"
                        value={formData.match_format}
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
                    <label>
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
                <hr className="createHr" />
                <div className="createBottom">
                    <button className="createButton">create</button>
                </div>
            </div>
        </form>
    );
};
