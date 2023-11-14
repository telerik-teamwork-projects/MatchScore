import "./tournamentFeed.scss";

import { CreateTournament } from "./createTournament/CreateTournament";
import { TournamentsList } from "./tournamentsList/TournamentsList";
import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../contexts/authContext";
import { getAll } from "../../services/tournamentService";

export const TournamentFeed = () => {
    const { user, token } = useContext(AuthContext);
    const [tournaments, setTournaments] = useState(null);

    useEffect(() => {
        try {
            const fetchData = async () => {
                const result = await getAll();
                setTournaments(result);
            };
            fetchData();
        } catch (error) {
            console.error(error);
        }
    }, []);

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
                <TournamentsList
                    user={user}
                    token={token}
                    tournaments={tournaments}
                />
            </div>
        </div>
    );
};
