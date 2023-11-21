import { Routes, Route } from "react-router-dom";

import { Home } from "./pages/home/Home";
import { Login } from "./pages/login/Login";
import { Register } from "./pages/register/Register";
import { Profile } from "./pages/profile/Profile";
import { ProfileUpdate } from "./pages/profileUpdate/ProfileUpdate";

import { Layout } from "./components/layout/Layout";
import { AuthProvider } from "./contexts/authContext";

import {
    HOME,
    LOGIN,
    PROFILE,
    REGISTER,
    TOURNAMENTS,
    PLAYERS,
} from "./routes/routes";

import { AuthRouteGuard } from "./routeGuards/authRouteGuard";
import { NoAuthRouteGuard } from "./routeGuards/noAuthRouteGuard";
import { Tournament } from "./pages/tournaments/Tournament";
import { TournamentDetails } from "./components/tournaments/tournamentDetails/TournamentDetails";
import { PlayerProfile } from "./components/playerProfile/PlayerProfile";

function App() {
    return (
        <AuthProvider>
            <Layout>
                <Routes>
                    <Route element={<NoAuthRouteGuard />}>
                        <Route path={LOGIN} element={<Login />} />
                        <Route path={REGISTER} element={<Register />} />
                    </Route>

                    <Route path={HOME} element={<Home />} />
                    <Route path={TOURNAMENTS} element={<Tournament />} />
                    <Route
                        path={`${TOURNAMENTS}/:tournamentId`}
                        element={<TournamentDetails />}
                    />

                    <Route
                        path={`${PLAYERS}/:playerId`}
                        element={<PlayerProfile />}
                    />

                    <Route element={<AuthRouteGuard />}>
                        <Route
                            path={`${PROFILE}/:userId`}
                            element={<Profile />}
                        />
                        <Route
                            path={`${PROFILE}/:userId/update`}
                            element={<ProfileUpdate />}
                        />
                    </Route>
                </Routes>
            </Layout>
        </AuthProvider>
    );
}

export default App;
