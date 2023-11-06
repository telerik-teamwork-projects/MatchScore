import "./leftbar.scss";
import HomeIcon from "@mui/icons-material/Home";
import ChatIcon from "@mui/icons-material/Chat";
import VideocamIcon from "@mui/icons-material/Videocam";
import GroupsIcon from "@mui/icons-material/Groups";
import EventNoteIcon from "@mui/icons-material/EventNote";

export const Leftbar = () => {
    return (
        <div className="leftbar">
            <div className="leftbarWrapper">
                <ul className="leftbarList">
                    <li className="leftbarListItem">
                        <HomeIcon className="icon" />
                        <span className="leftbarListItemText">Home</span>
                    </li>
                    <li className="leftbarListItem">
                        <ChatIcon className="icon" />
                        <span className="leftbarListItemText">Chat</span>
                    </li>
                    <li className="leftbarListItem">
                        <VideocamIcon className="icon" />
                        <span className="leftbarListItemText">Videos</span>
                    </li>
                    <li className="leftbarListItem">
                        <GroupsIcon className="icon" />
                        <span className="leftbarListItemText">Teams</span>
                    </li>
                    <li className="leftbarListItem">
                        <EventNoteIcon className="icon" />
                        <span className="leftbarListItemText">Schedule</span>
                    </li>
                </ul>
                <button className="leftbarButton">Show More</button>
                <hr className="leftbarHr" />
            </div>
        </div>
    );
};
