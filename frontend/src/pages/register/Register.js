import "./register.scss";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { register } from "../../services/authService";
import { ErrorMessage } from "../../components/responseMessages/errorMessages/ErrorMessages";
import { LOGIN } from "../../routes/routes";

export const Register = () => {
    const navigate = useNavigate();

    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        password2: "",
    });

    const { username, email, password, password2 } = formData;

    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const onRegister = async (e) => {
        e.preventDefault();

        try {
            await register({ username, email, password, password2 });
            navigate(LOGIN);
        } catch (error) {
            setError(error.response.data.detail);
        }
    };

    return (
        <>
            <div className="register">
                <div className="registerWrapper">
                    <div className="registerLeft">
                        <h3 className="registerLogo">MatchScore</h3>
                        <span className="registerDesc">
                            Join the community! Get started with MatchScore by
                            creating your account.
                        </span>
                    </div>
                    <div className="registerRight">
                        <form
                            className="registerBox"
                            onSubmit={(e) => onRegister(e)}
                        >
                            <input
                                placeholder="Username"
                                className="registerInput"
                                type="text"
                                name="username"
                                value={username}
                                onChange={(e) => onChange(e)}
                                required
                                autoComplete="username"
                            />

                            <input
                                placeholder="Email"
                                className="registerInput"
                                type="email"
                                name="email"
                                value={email}
                                onChange={(e) => onChange(e)}
                                required
                                autoComplete="email"
                            />

                            <input
                                placeholder="Password"
                                className="registerInput"
                                type="password"
                                name="password"
                                value={password}
                                onChange={(e) => onChange(e)}
                                required
                                autoComplete="text"
                            />

                            <input
                                placeholder="Confirm Password"
                                className="registerInput"
                                type="password"
                                name="password2"
                                value={password2}
                                onChange={(e) => onChange(e)}
                                required
                                autoComplete="text"
                            />
                            <ErrorMessage message={error} />

                            <button className="registerButton">Sign Up</button>
                            <Link className="linkLogin" to={"/login"}>
                                Log into Account
                            </Link>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
};
