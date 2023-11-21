import "./tournamentFeed.scss";

import { CreateTournamentModal } from "./createTournamentModal/CreateTournamentModal";
import { TournamentsList } from "./tournamentsList/TournamentsList";
import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../contexts/authContext";
import { getAll } from "../../services/tournamentService";

export const TournamentFeed = () => {
    const { user, token } = useContext(AuthContext);
    const [tournamentsData, setTournamentsData] = useState({
        tournaments: [],
        pagination: {
            page: 1,
            items_per_page: 10,
            total_pages: 1,
        },
    });

    const fetchData = async (page) => {
        try {
            const tournamentsResponse = await getAll(page);
            setTournamentsData(tournamentsResponse);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchData(tournamentsData.pagination.page);
    }, []);

    const handlePageChange = (pageNumber) => {
        fetchData(pageNumber);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    const [createModalOpen, setCreateModalOpen] = useState(false);

    const openCreateModal = () => {
        setCreateModalOpen(true);
    };

    const closeCreateModal = () => {
        setCreateModalOpen(false);
    };

    return (
        <div className="tournamentFeed">
            <div className="tournamentFeedWrapper">
                {(user?.role === "admin" || user?.role === "director") && (
                    <>
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
                    </>
                )}
                <h1 className="tournamentTitleMain">Tournaments</h1>
                <TournamentsList
                    user={user}
                    token={token}
                    handlePageChange={handlePageChange}
                    tournamentsData={tournamentsData}
                />
                {createModalOpen && (
                    <CreateTournamentModal
                        user={user}
                        token={token}
                        setTournaments={setTournamentsData.tournaments}
                        onClose={closeCreateModal}
                    />
                )}
            </div>
        </div>
    );
};
