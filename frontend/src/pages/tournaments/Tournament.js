import "./tournament.scss"

import { TournamentFeed } from "../../components/tournaments/TournamentFeed";

export const Tournament = ({ user, token }) => {
    return (
        <div className="tournament">
            <TournamentFeed user={user} token={token} />
        </div>
    );
};
