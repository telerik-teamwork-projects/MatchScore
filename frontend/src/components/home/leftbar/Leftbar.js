import "./leftbar.scss";
import { Link } from "react-router-dom";
import { TOURNAMENTS } from "../../../routes/routes";
import { useEffect, useState } from "react";
import { getAll } from "../../../services/tournamentService";

export const Leftbar = () => {
    const [tournaments, setTournaments] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const tournamentData = await getAll();
                setTournaments(tournamentData);
            } catch (error) {
                console.error(error);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="leftbar">
            <div className="leftbarWrapper">
                <Link className="leftbarLink" to={TOURNAMENTS}>
                    Tournaments
                </Link>
                <ul className="leftbarList">
                    {tournaments?.map((tournament) => (
                        <li key={tournament.id} className="leftbarListItem">
                            <Link to={`${TOURNAMENTS}/${tournament.id}`} className="link">
                                <span>{tournament.title}</span>
                            </Link>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};
