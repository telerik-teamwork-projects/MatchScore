import "./feed.scss";

import { Match } from "../../match/Match";
import { useEffect, useState } from "react";
import { getMatches } from "../../../services/matchesService";
import { Pagination } from "../../pagination/Pagination";

export const Feed = () => {
    const [matchesData, setMatchesData] = useState({
        matches: [],
        pagination: {
            page: 1,
            items_per_page: 10,
            total_pages: 1,
        },
    });

    const fetchData = async (page) => {
        try {
            const currentDate = new Date().toISOString();
            const matchesData = await getMatches(page, currentDate);
            setMatchesData(matchesData);
        } catch (error) {
            console.error(error);
        }
    };

    useEffect(() => {
        fetchData(matchesData.pagination.page);
    }, []);

    const handlePageChange = (pageNumber) => {
        fetchData(pageNumber);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    return (
        <div className="feed">
            <div className="feedWrapper">
                <div className="match">
                    {matchesData?.matches.map((match) => (
                        <Match match={match} key={match.id} />
                    ))}
                </div>
                {matchesData?.matches.length > 0 && (
                    <Pagination
                        handlePageChange={handlePageChange}
                        dataToFetch={matchesData}
                    />
                )}
            </div>
        </div>
    );
};
