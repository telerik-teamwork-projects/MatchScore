import "./profileUpdate.scss";
import { AuthErrorMessage } from "../../components/errorMessages/authErrorMessages";
import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect, useContext } from "react";
import { AuthContext } from "../../contexts/authContext";
import { getUser } from "../../services/authService";

export const ProfileUpdate = () => {
    const navigate = useNavigate();

    const { userUpdate, user } = useContext(AuthContext);

    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        bio: "",
        profile_img: null,
        cover_img: null,
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const userData = await getUser(user.id);
                setFormData({
                    username: userData.username || "",
                    email: userData.email || "",
                    bio: userData.bio || "",
                    role: userData.role || "",
                    profile_img: userData.profile_img || "",
                    cover_img: userData.cover_img || "",
                });
            } catch (error) {
                setError(error);
            }
        };
        fetchData();
    }, [user.id]);

    const { username, email, bio, role } = formData;

    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });
        
    const handleProfilePictureChange = (e) => {
        setFormData({ ...formData, profile_img: e.target.files[0] || null });
    };

    const handleCoverPictureChange = (e) => {
        setFormData({ ...formData, cover_img: e.target.files[0] || null });
    };

    const onSubmit = async (e) => {
        e.preventDefault();

        try {
            await userUpdate(formData, user?.id);
            navigate(`/profile/${user?.id}`);
        } catch (error) {
            setError(error.response.data.detail);
        }
    };

    return (
        <>
            <div className="profileUpdate">
                <div className="profileUpdateWrapper">
                    <div className="profileUpdateLeft">
                        <h3 className="profileUpdateLogo">Profile Update</h3>
                        <span className="profileUpdateDesc">
                            Let people know more about you
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
                                placeholder="Username"
                                className="profileUpdateInput"
                                type="text"
                                name="username"
                                value={username}
                                onChange={(e) => onChange(e)}
                                autoComplete="username"
                            />

                            <input
                                placeholder="Email"
                                className="profileUpdateInput"
                                type="email"
                                name="email"
                                value={email}
                                onChange={(e) => onChange(e)}
                                autoComplete="email"
                            />

                            <input
                                placeholder="Bio"
                                className="profileUpdateInput"
                                type="text"
                                name="bio"
                                value={bio}
                                onChange={(e) => onChange(e)}
                                autoComplete="text"
                            />
                            {user.role === "admin" && (
                                <input
                                    placeholder="Role"
                                    className="profileUpdateInput"
                                    type="text"
                                    name="role"
                                    value={role}
                                    onChange={(e) => onChange(e)}
                                    autoComplete="text"
                                />
                            )}

                            <label htmlFor="profile_img">
                                Profile Picture:
                                <input
                                    type="file"
                                    id="profile_img"
                                    name="profile_img"
                                    onChange={(e) => {
                                        handleProfilePictureChange(e);
                                    }}
                                />
                            </label>

                            <label htmlFor="cover_img">
                                Cover Picture:
                                <input
                                    type="file"
                                    id="cover_img"
                                    name="cover_img"
                                    onChange={(e) => {
                                        handleCoverPictureChange(e);
                                    }}
                                />
                            </label>
                            <AuthErrorMessage message={error} />

                            <button className="profileUpdateButton">
                                Update
                            </button>
                            <Link className="linkLogin" to={"/"}>
                                Back to Home
                            </Link>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
};
