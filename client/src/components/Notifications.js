import React, { useState, useEffect } from 'react';
import "./styles/Settings.css"

function Notifications() {









  useEffect(()=> {

    fetch('/notifications')
    .then((r)=> r.json())
    .then((d)=> {
 
    })


  },[])
  







  




  return (
    <div class="upload-container">
      
    </div>
  );
}
export default Notifications;
