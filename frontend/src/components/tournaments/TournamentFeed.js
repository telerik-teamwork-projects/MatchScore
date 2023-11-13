import "./tournamentFeed.scss";

import { CreateTournamentModal } from "./createTournamentModal/CreateTournamentModal";
import { TournamentsList } from "./tournamentsList/TournamentsList";
import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../contexts/authContext";
import { getAll } from "../../services/tournamentService";

export const TournamentFeed = () => {
    const { user, token } = useContext(AuthContext);
    const [tournaments, setTournaments] = useState(null);
    const [createModalOpen, setCreateModalOpen] = useState(false);

    const openCreateModal = () => {
        setCreateModalOpen(true);
    };

    const closeCreateModal = () => {
        setCreateModalOpen(false);
    };

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
                <div className="tournamentTop">
                    <button
                        className="createTournamentBtn"
                        type="button"
                        onClick={openCreateModal}
                    >
                        Create Tournament
                    </button>
                </div>
                <hr className="tournamentHr" />
                <h1 className="tournamentTitleMain">Tournaments</h1>
                <TournamentsList
                    user={user}
                    token={token}
                    tournaments={tournaments}
                />
                {createModalOpen && (
                    <CreateTournamentModal
                        user={user}
                        token={token}
                        setTournaments={setTournaments}
                        onClose={closeCreateModal}
                    />
                )}
            </div>
        </div>
    );
};
