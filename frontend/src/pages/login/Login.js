import "./login.scss";
import { Link, useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import { AuthContext } from "../../components/contexts/authContext";
import { AuthErrorMessage } from "../../components/errorMessages/authErrorMessages";
import { HOME } from "../../routes/routes";

export const Login = () => {
    const navigate = useNavigate();
    const { userLogin } = useContext(AuthContext);
    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const { email, password } = formData;

    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const onLogin = async (e) => {
        e.preventDefault();

        try {
            await userLogin({ email, password });
            navigate(HOME);
        } catch (error) {
            formData.email = "";
            formData.password = "";
            setError(error.response.data.error);
        }
    };

    return (
        <div className="login">
            <div className="loginWrapper">
                <div className="loginLeft">
                    <h3 className="loginLogo">MatchScore</h3>
                    <span className="loginDesc">
                        Welcome back! Let's get started.
                    </span>
                </div>
                <div className="loginRight">
                    <form className="loginBox" onSubmit={(e) => onLogin(e)}>
                        <input
                            placeholder="Email"
                            className="loginInput"
                            type="email"
                            name="email"
                            value={email}
                            onChange={(e) => onChange(e)}
                            required
                            autoComplete="email"
                        />
                        <input
                            placeholder="Password"
                            className="loginInput"
                            type="password"
                            name="password"
                            value={password}
                            onChange={(e) => onChange(e)}
                            required
                            autoComplete="text"
                        />

                        <AuthErrorMessage message={error} />

                        <button className="loginButton">Log in</button>
                        <Link to={"/register"} className="linkRegister">
                            Create a new Account
                        </Link>
                    </form>
                </div>
            </div>
        </div>
    );
};
