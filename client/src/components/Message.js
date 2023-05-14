import React from 'react';
import './styles/Comment.css';

const Message = ({ username, content, timestamp, avatar }) => {
  return (
    <div className="comment">
      <div className="comment-header">
        <img className="profile-pic" src={avatar} alt="Author's profile" />
        <h3 className="comment-author">{username}</h3>
      </div>
      <p className="comment-text">{content}</p>
      <p className="comment-timestamp">{new Date(timestamp).toLocaleString()}</p>
    </div>
  );
};

export default Message;
