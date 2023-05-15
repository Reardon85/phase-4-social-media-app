import React, { useState, useEffect } from 'react';
import "./styles/CommentForm.css";
import Message from './Message';


const MessageForm = ({ convoId }) => {
  const [message, setMessage] = useState('');
  const [messageList, setMessageList] = useState([])

  console.log(convoId)

  useEffect(() => {

    fetch(`/message/${convoId}`)
      .then((r) => r.json())
      .then((d) => setMessageList(d))


  }, [convoId])
  

  const comment_array = messageList.map((c) => {
    return <Message key={c.id} username={c.username} avatar={c.avatar_url} timestamp={c.created_at} content={c.text} userId={c.user_id} />
  })

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you would handle the comment submission, for instance, by calling an API endpoint.
    
    const message_info = {
      convoId: convoId,
      text: message,
    }

    fetch(`/message/${convoId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(message_info)
    }).then((r) => r.json())
      .then((d) => setMessageList((messageList) => messageList.concat(d)))


    setMessage('');
  }





  return (
    <>
      {comment_array}
      <form className="comment-form" onSubmit={handleSubmit}>
        <textarea
          className="comment-input"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Write your comment..."
        />
        <button className="com-btn" type="submit">Submit</button>
      </form>
    </>
  );
};

export default MessageForm;