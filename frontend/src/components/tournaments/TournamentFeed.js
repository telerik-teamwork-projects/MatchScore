import "./tournamentFeed.scss";

import { CreateKnockoutModal } from "./createTournamentModal/CreateKnockoutModal";
import { TournamentsList } from "./tournamentsList/TournamentsList";
import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../contexts/authContext";
import { getAll } from "../../services/tournamentService";
import { CreateLeagueModal } from "./createTournamentModal/CreateLeagueModal";

export const TournamentFeed = () => {
    const { user, token } = useContext(AuthContext);
    const [tournamentsData, setTournamentsData] = useState({
        tournaments: [],
        pagination: {
            page: 1,
            items_per_page: 10,
            total_pages: 1,
        },
        loading: true,
    });

    const fetchData = async (page) => {
        try {
            const tournamentsResponse = await getAll(page);
            setTournamentsData({ ...tournamentsResponse, loading: false });
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchData(tournamentsData.pagination.page);
    }, [tournamentsData.pagination.page]);

    const handlePageChange = (pageNumber) => {
        fetchData(pageNumber);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    const [createKnockoutModalOpen, setCreateKnockoutModalOpen] =
        useState(false);
    const [createLeagueModalOpen, setCreateLeagueModalOpen] = useState(false);

    const openKnockoutCreateModal = () => {
        setCreateKnockoutModalOpen(true);
    };

    const openLeagueCreateModal = () => {
        setCreateLeagueModalOpen(true);
    };

    const closeKnockoutCreateModal = () => {
        setCreateKnockoutModalOpen(false);
    };

    const closeLeagueCreateModal = () => {
        setCreateLeagueModalOpen(false);
    };

    return (
        <div className="tournamentFeed">
            <div className="tournamentFeedWrapper">
                {(user?.role === "admin" || user?.role === "director") && (
                    <>
                        <div className="tournamentTop">
                            <button
                                className="createKnockoutBtn"
                                type="button"
                                onClick={openKnockoutCreateModal}
                            >
                                Create Knockout Tournament
                            </button>
                            <button
                                className="createLeagueBtn"
                                type="button"
                                onClick={openLeagueCreateModal}
                            >
                                Create League Tournament
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
                    loading={tournamentsData.loading}
                />
                {createKnockoutModalOpen && (
                    <CreateKnockoutModal
                        user={user}
                        token={token}
                        setTournaments={setTournamentsData.tournaments}
                        onClose={closeKnockoutCreateModal}
                    />
                )}

                {createLeagueModalOpen && (
                    <CreateLeagueModal
                        user={user}
                        token={token}
                        setTournaments={setTournamentsData.tournaments}
                        onClose={closeLeagueCreateModal}
                        loadn
                    />
                )}
            </div>
        </div>
    );
};
