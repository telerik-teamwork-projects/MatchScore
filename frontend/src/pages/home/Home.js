import "./home.scss";

import { Leftbar } from "../../components/home/leftbar/Leftbar";
import { Feed } from "../../components/home/feed/Feed";

export const Home = () => {
    return (
        <div className="home">
            <Leftbar />
            <Feed />
        </div>
    );
};
