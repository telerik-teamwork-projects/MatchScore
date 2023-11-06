import "./footer.scss";

export const Footer = () => {
    return (
        <div className="footer">
            <div className="footerWrapper">
                <div className="top">
                    <div className="item">
                        <h1 className="title">Sports</h1>
                        <span className="span">Football</span>
                        <span className="span">Basketball</span>
                        <span className="span">Tennis</span>
                        <span className="span">Volleyball</span>
                    </div>
                    <div className="item">
                        <h1 className="title">Links</h1>
                        <span className="span">Schedule</span>
                        <span className="span">Results</span>
                        <span className="span">Teams</span>
                        <span className="span">Tickets</span>
                        <span className="span">Sponsors</span>
                    </div>
                    <div className="item">
                        <h1 className="title">About</h1>
                        <span className="span">
                            Lorem ipsum dolor sit amet, consectetur adipiscing
                            elit. The sporting tournament brings together the
                            best athletes from around the world to compete in
                            various sports.
                        </span>
                    </div>
                    <div className="item">
                        <h1 className="title">Contact</h1>
                        <span className="span">
                            For inquiries and support, please contact us at
                            info@sportingtournament.com or call +1-123-456-7890.
                        </span>
                    </div>
                </div>
                <div className="bottom">
                    <span className="logo">
                        <img src="/images/matchscore.png" alt="logo" />
                    </span>
                    <span className="copyright">
                        © Sporting Tournament 2023. All Rights Reserved
                    </span>
                </div>
            </div>
        </div>
    );
};
