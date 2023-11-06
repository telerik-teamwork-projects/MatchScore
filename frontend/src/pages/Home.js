import { Leftbar } from "../components/home/leftbar/Leftbar";
import { Rightbar } from "../components/home/rightbar/Rightbar";
import { Feed } from "../components/home/feed/Feed";

export const Home = () => {
    return (
        <div className="home">
            <Leftbar />
            <Feed />
            <Rightbar />
        </div>
    );
};
