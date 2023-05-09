
import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import "./styles/SideBar.css"

function SideBar({onLogout, user}) {

    const navigate = useNavigate()
    console.log(user.id)

    const handleclick = () => {

        fetch('/logout', {
            method: "DELETE",
        }).then((r) =>{
            if (r.ok){
                onLogout("none")
                navigate("/")
            }
        })

    }


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
            <NavLink to={`/profile/${user.id}`} activeClassName="active">
                Profile
            </NavLink>
            <NavLink to="/search" activeClassName="active">
                Search
            </NavLink>
            <NavLink onClick={handleclick} to="/logout" activeClassName="active">
                Logout
            </NavLink>
        </div>
    );
}

export default SideBar;
