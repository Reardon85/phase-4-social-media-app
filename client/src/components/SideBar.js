
import React from 'react';
import { NavLink } from 'react-router-dom';
import { Link } from 'react-router-dom';
import "./styles/SideBar.css"

function SideBar() {
    return (
        <div className="sidebar">
            <Link to="/">
                <div className="logo-container">
                    <h1 className="logo">The Tea</h1>
                    <img
                        src="/images/logo1.png"
                        alt="Logo"
                        className="logo-img"
                        width="30px"
                        height="30px"
                    />
                </div>
            </Link>

            <NavLink exact to="/" activeClassName="active">
                Home
            </NavLink>
            <NavLink to="/foryou" activeClassName="active">
                For You
            </NavLink>
            <NavLink to="/profile" activeClassName="active">
                Profile
            </NavLink>
            <NavLink to="/search" activeClassName="active">
                Search
            </NavLink>
            <NavLink to="/Logout" activeClassName="active">
                Logout
            </NavLink>
        </div>
    );
}

export default SideBar;
