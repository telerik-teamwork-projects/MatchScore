import "./tournamentFeed.scss";

import { CreateTournament } from "./createTournament/CreateTournament";
import { TournamentsList } from "./tournamentsList/TournamentsList";
import { useContext, useState } from "react";
import { AuthContext } from "../../contexts/authContext";

export const TournamentFeed = () => {
    const { user, token } = useContext(AuthContext);
    const [tournaments, setTournaments] = useState(null);

    return (
        <div className="tournamentFeed">
            <div className="tournamentFeedWrapper">
                <CreateTournament
                    user={user}
                    token={token}
                    setTournaments={setTournaments}
                />
                <hr className="tournamentHr" />
                <h1 className="tournamentTitleMain">Tournaments</h1>
                <TournamentsList user={user} tournaments={tournaments} />
            </div>
        </div>
    );
};
