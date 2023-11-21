import "./home.scss";

import { Leftbar } from "../../components/home/leftbar/Leftbar";
import { Feed } from "../../components/home/feed/Feed";
import { Rightbar } from "../../components/home/rightbar/Rightbar";

export const Home = () => {
    return (
        <div className="home">
            <Leftbar />
            <Feed />
            <Rightbar />
        </div>
    );
};
