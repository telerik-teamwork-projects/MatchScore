import "./participantCelection.scss";

import { useState, useEffect } from "react";
import { getAll } from "../../services/playerService";
import { Pagination } from "../pagination/Pagination";

export const ParticipantSelection = ({
    selectedPlayers,
    onPlayerSelection,
    onClose,
}) => {
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

    const [selected, setSelected] = useState(selectedPlayers);

    const handleCheckboxChange = (playerId) => {
        if (selected.includes(playerId)) {
            setSelected(selected.filter((id) => id !== playerId));
        } else {
            setSelected([...selected, playerId]);
        }
    };

    const handleSave = () => {
        onPlayerSelection(selected);
    };

    return (
        <div className="participantSelectionModal">
            <h2>Select Participants</h2>
            <ul>
                {playersData?.players.map((player) => (
                    <li key={player.id}>
                        <input
                            name="playerSelect"
                            type="checkbox"
                            checked={selected.includes(player.id)}
                            onChange={() => handleCheckboxChange(player.id)}
                        />
                        {player.full_name}
                    </li>
                ))}
            </ul>
            <Pagination
                handlePageChange={handlePageChange}
                dataToFetch={playersData}
            />
            <div className="participantSelBtns">
                <button className="participantsSave" onClick={handleSave}>Save</button>
                <button className="participantsCancel" onClick={onClose}>Cancel</button>
            </div>
        </div>
    );
};
