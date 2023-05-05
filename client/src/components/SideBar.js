
import React from 'react';
import { NavLink } from 'react-router-dom';
import "./SideBar.css"

function SideBar() {
    return (
        <div className="sidebar">
            <NavLink exact to="/" activeClassName="active">
                Home
            </NavLink>
            <NavLink to="/foryou" activeClassName="active">
                For You
            </NavLink>
            <NavLink to="/profile" activeClassName="active">
                Profile
            </NavLink>
        </div>
    );
}

export default SideBar;
