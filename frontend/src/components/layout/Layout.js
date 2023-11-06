import "./layout.scss";

import { Navbar } from "../navbar/Navbar";
import { Footer } from "../footer/Footer";

export const Layout = ({ children }) => {
    return (
        <div className="layout">
            <Navbar />
            {children}
            <Footer />
        </div>
    );
};
