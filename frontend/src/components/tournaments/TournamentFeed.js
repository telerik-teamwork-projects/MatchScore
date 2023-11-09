import "./tournamentFeed.scss"

import { CreateTournament } from "../createTournament/CreateTournament";

export const TournamentFeed = ({ user, token }) => {
    return (
        <div className="tournamentFeed">
            <div className="tournamentFeedWrapper">
                <CreateTournament user={user} token={token} />
            </div>
        </div>
    );
};
