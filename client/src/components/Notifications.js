import React, { useState, useEffect } from 'react';
import "./styles/Notifications.css"
import { Link } from 'react-router-dom';

function Notifications() {


const [notificationList, setNotificationList] = useState([])





  useEffect(()=> {

    fetch('/notification')
    .then((r)=> r.json())
    .then((d)=> {

      setNotificationList(d)
 
    })


  },[])





    const notificationArray = notificationList.map((n) => ( 
      <div className={n.seen === true ? 'notification-div' : 'notification-div-unseen'}> 
        <Link to={`/profile/${n.action_user_id}`}   style={{ textDecoration: 'none', color: 'inherit' }}>
          <img src={n.avatar_url} alt=''  className='user-notification-photo'/>
        </Link>
        {n.username}
        {n.action} 
        {n.image.length > 0 ? <Link to={`/posts/${n.post_id}`}><img src={n.image} alt='' className='post-notification-photo' /></Link> : ''}
      </div>
    ) )




  







  




  return (
    <div class="notification-container">

      {notificationArray}
      
    </div>
  );
}
export default Notifications;
