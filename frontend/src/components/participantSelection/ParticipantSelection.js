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

    const [fullName, setFullName] = useState("");
    const [selected, setSelected] = useState(selectedPlayers);

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
    }, [playersData.pagination.page]);

    const handlePageChange = (pageNumber) => {
        fetchData(pageNumber);
    };

    const handleCheckboxChange = (playerId) => {
        setSelected((prevSelected) => {
            const isPlayerSelected = prevSelected.some(
                (player) => player.id === playerId
            );
            if (isPlayerSelected) {
                return prevSelected.filter((player) => player.id !== playerId);
            } else {
                const playerToAdd = playersData.players.find(
                    (player) => player.id === playerId
                );
                return [...prevSelected, playerToAdd];
            }
        });
    };

    const handleSave = () => {
        const newPlayer = fullName.trim();

        if (selected.length === 0 && newPlayer === "") {
            return;
        }

        const selectedPlayerDetails = selected.map((selPlayer) => {
            const player = playersData.players.find(
                (p) => p.id === selPlayer.id
            );
            return {
                id: selPlayer.id,
                full_name: player?.full_name,
            };
        });
        const newPlayerDetails = newPlayer
            ? {
                  full_name: newPlayer,
              }
            : null;

        onPlayerSelection(selectedPlayerDetails, newPlayerDetails);
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
                            checked={selected.some((p) => p.id === player.id)}
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
            <div className="playerNameInput">
                <input
                    type="text"
                    name="full_name"
                    placeholder="Full Name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    autoComplete="text"
                />
            </div>
            <div className="participantSelBtns">
                <button className="participantsSave" onClick={handleSave}>
                    Save
                </button>
                <button className="participantsCancel" onClick={onClose}>
                    Cancel
                </button>
            </div>
        </div>
    );
};
