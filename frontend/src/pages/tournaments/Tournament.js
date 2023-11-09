import "./tournament.scss"

import { Leftbar } from "../../components/home/leftbar/Leftbar";
import { TournamentFeed } from "../../components/tournaments/TournamentFeed";

export const Tournament = ({ user, token }) => {
    return (
        <div className="tournament">
            <Leftbar />
            <TournamentFeed user={user} token={token} />
        </div>
    );
};
