import "./rightbar.scss";
import { Link } from "react-router-dom";
import { PLAYERS } from "../../../routes/routes";
import { useEffect, useState } from "react";
import { getAll } from "../../../services/playerService";
import { Pagination } from "../../pagination/Pagination";

export const Rightbar = () => {
    const [playersData, setPlayersData] = useState({
        players: [],
        pagination: {
            page: 1,
            items_per_page: 10,
            total_pages: 1,
        },
    });

    const fetchData = async (page) => {
        try {
            const playersResponse = await getAll(page);
            setPlayersData(playersResponse);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchData(playersData.pagination.page);
    }, []);

    const handlePageChange = (pageNumber) => {
        fetchData(pageNumber);
    };

    return (
        <div className="rightbar">
            <div className="rightbarWrapper">
                <p className="rightbarTitle">Players</p>
                <ul className="rightbarList">
                    {playersData?.players.map((player) => (
                        <li key={player.id} className="rightbarListItem">
                            <Link
                                to={`${PLAYERS}/${player.id}`}
                                className="link"
                            >
                                <span>{player.full_name}</span>
                            </Link>
                        </li>
                    ))}
                </ul>
                <Pagination
                    handlePageChange={handlePageChange}
                    dataToFetch={playersData}
                />
            </div>
        </div>
    );
};
