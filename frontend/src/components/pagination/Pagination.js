import "./pagination.scss";

export const Pagination = ({ handlePageChange, dataToFetch }) => {
    const { page, total_pages } = dataToFetch.pagination;

    const getDisplayedPages = () => {
        const range = 1;
        const start = Math.max(1, page - range);
        const end = Math.min(total_pages, page + range);

        return [...Array(end - start + 1).keys()].map((i) => start + i);
    };

    return (
        <div className="pagination">
            <div
                onClick={() => handlePageChange(page - 1)}
                className="paginationNumber"
            >
                Prev
            </div>
            {getDisplayedPages().map((pageNumber) => (
                <div
                    key={pageNumber}
                    onClick={() => handlePageChange(pageNumber)}
                    className={
                        pageNumber === page
                            ? "paginationNumber paginationNumber--active"
                            : "paginationNumber"
                    }
                >
                    {pageNumber}
                </div>
            ))}

            <div
                onClick={() => handlePageChange(page + 1)}
                className="paginationNumber"
            >
                Next
            </div>
        </div>
    );
};
