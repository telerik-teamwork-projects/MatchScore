import "./match.scss";

export const Match = () => {
    return (
        <div className="match">
            <div className="matchWrapper">
                <div className="matchContainer">
                    <div className="matchBox">
                        <div className="matchHeader">
                            <div className="matchHeaderLeft">
                                <span>Live</span>
                            </div>
                            <div className="matchHeaderRight">
                                <span>20 mins ago</span>
                            </div>
                        </div>
                        <hr />
                        <div className="matchMain">
                            <span className="matchTitle">
                                Champions league semi-final
                            </span>
                            <div className="matchTeam">
                                <div className="teamInfo">
                                    <img src="/images/teams/manchester-city.png" />
                                    <span className="Team1">
                                        Machester City
                                    </span>
                                </div>
                                <span className="teamScore">1</span>
                            </div>
                            <div className="matchTeam">
                                <div className="teamInfo">
                                    <img src="/images/teams/liverpool.png" />
                                    <span>Liverpool</span>
                                </div>
                                <span className="teamScore">0</span>
                            </div>
                            <span className="matchTime">
                                Etihad Stadium, Manchester
                            </span>
                        </div>
                        <hr />
                        <div className="matchBottom">
                            <button className="actionButton">Watch Live</button>
                        </div>
                    </div>

                    <div className="matchBox">
                        <div className="matchHeader">
                            <div className="matchHeaderLeft">
                                <span>Live</span>
                            </div>
                            <div className="matchHeaderRight">
                                <span>20 mins ago</span>
                            </div>
                        </div>
                        <hr />
                        <div className="matchMain">
                            <span className="matchTitle">
                                Champions league semi-final
                            </span>
                            <div className="matchTeam">
                                <div className="teamInfo">
                                    <img src="/images/teams/manchester-city.png" />
                                    <span className="Team1">
                                        Machester City
                                    </span>
                                </div>
                                <span className="teamScore">1</span>
                            </div>
                            <div className="matchTeam">
                                <div className="teamInfo">
                                    <img src="/images/teams/liverpool.png" />
                                    <span>Liverpool</span>
                                </div>
                                <span className="teamScore">0</span>
                            </div>
                            <span className="matchTime">
                                Etihad Stadium, Manchester
                            </span>
                        </div>
                        <hr />
                        <div className="matchBottom">
                            <button className="actionButton">Watch Live</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
