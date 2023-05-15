import React, { useState, useEffect } from 'react';

import MessageForm from './MessageForm'
import "./styles/MessageCenter.css";

function MessageCenter() {

    const [conversations, setConversations] = useState([])
    const [convoId, setConvoId] = useState(null)

    useEffect(() => {

        fetch(`/message`)
            .then((r) => r.json())
            .then((d)=> {
              setConversations(d.list)
              setConvoId(d['convo_id'])
            })

    }, [])


    
    console.log("hello")
    const convoArray = conversations.map((convo) => (
      <div className='conversation-div' onClick={()=> setConvoId(convo.id)}>
        <img src={convo.avatar_url} alt='profile' className='user-convo-photo' />
        {convo.username}
      </div>
    ))
    
    return (
      <div className="discussion-container">
        <div className="discussion-card">
          {convoArray}
        </div>
        <div className="message-form-container">
          <MessageForm convoId={convoId} />
        </div>
      </div>
    );
}

export default MessageCenter;