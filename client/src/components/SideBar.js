
import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate, useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
import "./styles/SideBar.css"
import Search from './Search';
import Logo from './Logo';
import SearchResult from './SearchResult';

function SideBar({ onLogout, user }) {


    const navigate = useNavigate()
    
    const [activeNotification, setActiveNotification] = useState([false, false])

    



    useEffect(() => {



        fetch('/active-notifications')
            .then((r) => r.json())
            .then((d) => setActiveNotification([d['notifActive'], d['convoActive']]))



    }, [navigate])
   

    const handleclick = () => {

        fetch('/logout', {
            method: "DELETE",
        }).then((r) => {
            if (r.ok) {
                onLogout("none")
                navigate("/")
            }
        })

    }

    console.log(activeNotification)

    return (
        <div className="sidebar">
            <Link to="/">
                <div className="logo-container">
                    <h1 className="logo">The Tea</h1>
                    <img className='logo-img' src='/mstile-150x150.png'></img>
                </div>
            </Link>
            <Search />

            <NavLink exact to="/" activeClassName="active">
                <img src="/images/home.png" alt="Home Icon" className='icons' /> Home
            </NavLink>


            <NavLink to="/foryou" activeClassName="active">
                <img src="/images/foryou.png" alt="Home Icon" className='icons' /> For You
            </NavLink>

            <NavLink to={`/profile/${user.id}`} activeClassName="active">

                <img src="/images/profile.png" alt="Home Icon" className='icons' /> Profile

            </NavLink>

            <NavLink exact to="/notifications" activeClassName="active" className={activeNotification[0] ? 'active-notify' : 'inactive-notify'}>
                <img src={activeNotification[0] ? "/images/notification-active.png" : "/images/notification.png"} alt="Home Icon" className='icons' /> Notifications
            </NavLink>

            <NavLink exact to="/messages" activeClassName="active" className={activeNotification[1] ? 'active-notify' : 'inactive-notify'}>
                <img src={activeNotification[1] ? "/images/message-active.png" : "/images/message.png"} alt="Home Icon" className='icons' /> Messages
            </NavLink>

            <NavLink to={`/create`} activeClassName="active">

                <img src="/images/plus.png" alt="Home Icon" className='icons' /> Create Post

            </NavLink>





            <NavLink onClick={handleclick} to="/logout" activeClassName="active">
                Logout
            </NavLink>
        </div>
    );
}

export default SideBar;
