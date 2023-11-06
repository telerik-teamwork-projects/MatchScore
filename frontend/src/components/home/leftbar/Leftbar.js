import "./leftbar.scss";

export const Leftbar = () => {
    return (
        <div className="leftbar">
            <div className="leftbarWrapper">
                <h3>Tournaments</h3>
                <ul className="leftbarList">
                    <li className="leftbarListItem">
                        <div className="leftbarListItemContainer">
                            <span>Champions League</span>
                            <span>All stars</span>
                            <span>Grand Prix</span>
                        </div>
                    </li>
                </ul>

                <h3>Sports</h3>
                <ul className="leftbarList">
                    <li className="leftbarListItem">
                        <div className="leftbarListItemContainer">
                            <span>Football</span>
                            <span>Basketball</span>
                            <span>Volleyball</span>
                            <span>Baseball</span>
                            <span>Tennis</span>
                            <span>Box</span>
                            <span>America Football</span>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    );
};
