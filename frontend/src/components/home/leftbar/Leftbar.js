import "./leftbar.scss";
import { Link } from "react-router-dom";
import { TOURNAMENTS } from "../../../routes/routes";
import { useEffect, useState } from "react";
import { getAll } from "../../../services/tournamentService";
import { Pagination } from "../../pagination/Pagination";
import { FadeLoader } from "react-spinners";

export const Leftbar = () => {
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
    };

    return (
        <div className="leftbar">
            <div className="leftbarWrapper">
                <Link className="leftbarLink" to={TOURNAMENTS}>
                    Tournaments
                </Link>
                <ul className="leftbarList">
                    {tournamentsData.loading ? (
                        <div className="spinner-container">
                            <FadeLoader color="darkgray" loading={true} />
                        </div>
                    ) : (
                        tournamentsData.tournaments.map((tournament) => (
                            <li key={tournament.id} className="leftbarListItem">
                                <Link
                                    to={`${TOURNAMENTS}/${tournament.id}`}
                                    className="link"
                                >
                                    <span>{tournament.title}</span>
                                </Link>
                            </li>
                        ))
                    )}
                </ul>
            </div>
            <Pagination
                handlePageChange={handlePageChange}
                dataToFetch={tournamentsData}
            />
        </div>
    );
};
