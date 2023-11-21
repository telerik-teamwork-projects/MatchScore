import "./playerProfileUpdate.scss";
import { ErrorMessage } from "../../components/responseMessages/errorMessages/ErrorMessages";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../../contexts/authContext";
import { getOne, playerUpdate } from "../../services/playerService";
import { PLAYERS } from "../../routes/routes";

export const PlayerProfileUpdate = () => {
    const navigate = useNavigate();

    const { playerId } = useParams();
    const { token } = useContext(AuthContext);

    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        full_name: "",
        country: "",
        sports_club: "",
        profile_img: null,
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const playerData = await getOne(playerId);
                setFormData({
                    full_name: playerData.full_name || "",
                    country: playerData.country || "",
                    sports_club: playerData.sports_club || "",
                    profile_img: playerData.profile_img || "",
                });
            } catch (error) {
                setError(error);
            }
        };
        fetchData();
    }, [playerId]);

    const { full_name, country, sports_club } = formData;

    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const handleProfilePictureChange = (e) => {
        setFormData({ ...formData, profile_img: e.target.files[0] || null });
    };

    const onSubmit = async (e) => {
        e.preventDefault();
        try {
            await playerUpdate(playerId, token, formData);
            navigate(`${PLAYERS}/${playerId}`);
        } catch (error) {
            setError(error.response.data.detail);
        }
    };

    return (
        <>
            <div className="profileUpdate">
                <div className="profileUpdateWrapper">
                    <div className="profileUpdateLeft">
                        <h3 className="profileUpdateLogo">
                            Player Profile Update
                        </h3>
                        <span className="profileUpdateDesc">
                            Update your player profile
                        </span>
                    </div>
                    <div className="profileUpdateRight">
                        <form
                            className="profileUpdateBox"
                            method="post"
                            onSubmit={(e) => onSubmit(e)}
                            encType="multipart/form-data"
                        >
                            <input
                                placeholder="Full Name"
                                className="profileUpdateInput"
                                type="text"
                                name="full_name"
                                value={full_name}
                                onChange={(e) => onChange(e)}
                                autoComplete="text"
                            />

                            <input
                                placeholder="Country"
                                className="profileUpdateInput"
                                type="text"
                                name="country"
                                value={country}
                                onChange={(e) => onChange(e)}
                                autoComplete="country"
                            />

                            <input
                                placeholder="Sports Club"
                                className="profileUpdateInput"
                                type="text"
                                name="sports_club"
                                value={sports_club}
                                onChange={(e) => onChange(e)}
                                autoComplete="text"
                            />

                            <label htmlFor="profile_img">
                                Player Profile Picture:
                                <input
                                    type="file"
                                    id="profile_img"
                                    name="profile_img"
                                    onChange={(e) => {
                                        handleProfilePictureChange(e);
                                    }}
                                />
                            </label>

                            <ErrorMessage message={error} />

                            <button className="profileUpdateButton">
                                Update
                            </button>
                            <Link
                                className="linkLogin"
                                to={`${PLAYERS}/${playerId}`}
                            >
                                Back to Player Profile
                            </Link>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
};
