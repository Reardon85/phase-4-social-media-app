
import React from 'react';
import { NavLink } from 'react-router-dom';
import "./styles/SideBar.css"

function SideBar() {
    return (
        <div className="sidebar">
            <h1 className='logo'>The Tea</h1>
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
