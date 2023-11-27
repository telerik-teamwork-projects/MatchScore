import "./editTournamentPlayers.scss";
import { useEffect, useState } from "react";
import {
    updatePlayers,
    getPlayersByTournamentId,
} from "../../services/tournamentService";
import { Link } from "react-router-dom";
import { PLAYERS } from "../../routes/routes";

export const EditTournamentPlayers = ({ tournamentId, token, onClose }) => {
    const [players, setPlayers] = useState(null);
    const [formData, setFormData] = useState({
        player: "",
        player_prev: "",
    });

    useEffect(() => {
        const fetchPlayers = async () => {
            try {
                const playersData = await getPlayersByTournamentId(
                    tournamentId,
                    token
                );
                setPlayers(playersData);
            } catch (error) {
                console.error(error);
            }
        };
        fetchPlayers();
    }, [tournamentId, token]);

    const onChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const onUpdatePlayers = async (e) => {
        e.preventDefault();

        try {
            await updatePlayers(tournamentId, token, [formData]);
            onClose();
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div className="editPlayersModal">
            <div className="editPlayersContainer">
                <h3>Change Players</h3>
                <div className="editPlayersList">
                    <ul>
                        {players?.map((player) => (
                            <Link
                                key={player.id}
                                className="link"
                                to={`${PLAYERS}/${player.id}`}
                            >
                                <li>{player.full_name}</li>
                            </Link>
                        ))}
                    </ul>
                </div>

                <form
                    className="editPlayersForm"
                    onSubmit={(e) => onUpdatePlayers(e)}
                >
                    <input
                        placeholder="Old Player"
                        className="playerInput"
                        type="text"
                        name="player_prev"
                        value={formData.player_prev}
                        onChange={(e) => onChange(e)}
                        required
                    />
                    <input
                        placeholder="New Player"
                        className="playerInput"
                        type="text"
                        name="player"
                        value={formData.player}
                        onChange={(e) => onChange(e)}
                        required
                    />

                    <div className="editPlayersBtns">
                        <button className="submitBtn" type="submit">
                            Change Players
                        </button>
                        <button
                            className="closeBtn"
                            type="button"
                            onClick={onClose}
                        >
                            Close
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};
