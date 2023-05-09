
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
                <img src="./images/home.png" alt="Home Icon" className='icons' /> Home
            </NavLink>
            <NavLink to="/foryou" activeClassName="active">
                <img src="./images/foryou.png" alt="Home Icon" className='icons' /> For You
            </NavLink>
            <NavLink to="/profile" activeClassName="active">
                <img src="./images/profile.png" alt="Home Icon" className='icons' /> Profile
            </NavLink>
            <NavLink to="/search" activeClassName="active">
                <img src="./images/search.png" alt="Home Icon" className='icons' />Search
            </NavLink>
            <NavLink to="/Logout" activeClassName="active">
                Logout
            </NavLink>
        </div>
    );
}

export default SideBar;
