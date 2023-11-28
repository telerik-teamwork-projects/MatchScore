import "./rightbar.scss";
import { Link } from "react-router-dom";
import { PLAYERS } from "../../../routes/routes";
import { useEffect, useState } from "react";
import { getAll } from "../../../services/playerService";
import { Pagination } from "../../pagination/Pagination";
import { FadeLoader } from "react-spinners";

export const Rightbar = () => {
    const [playersData, setPlayersData] = useState({
        players: [],
        pagination: {
            page: 1,
            items_per_page: 10,
            total_pages: 1,
        },
        loading: true,
    });

    const fetchData = async (page) => {
        try {
            const playersResponse = await getAll(page);
            setPlayersData({ ...playersResponse, loading: false });
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchData(playersData.pagination.page);
    }, [playersData.pagination.page]);

    const handlePageChange = (pageNumber) => {
        fetchData(pageNumber);
    };

    return (
        <div className="rightbar">
            <div className="rightbarWrapper">
                <p className="rightbarTitle">Players</p>
                <ul className="rightbarList">
                    {playersData.loading ? (
                        <div className="spinner-container">
                            <FadeLoader color="darkgray" loading={true} />
                        </div>
                    ) : (
                        playersData?.players.map((player) => (
                            <li key={player.id} className="rightbarListItem">
                                <Link
                                    to={`${PLAYERS}/${player.id}`}
                                    className="link"
                                >
                                    <span>{player.full_name}</span>
                                </Link>
                            </li>
                        ))
                    )}
                </ul>
                <Pagination
                    handlePageChange={handlePageChange}
                    dataToFetch={playersData}
                />
            </div>
        </div>
    );
};
