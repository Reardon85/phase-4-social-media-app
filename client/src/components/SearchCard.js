import React from 'react'
import "./styles/SearchResult.css"

function SearchCard({ avatar_url, id, username, handleClick }) {


    return (
        <div onClick={() => handleClick(id)} className="voice-chat-card">
            <div className="voice-chat-card-header">
                <img className="avatar" alt="User avatar" src={avatar_url} />
                <div className="username">{username}</div>
                <div className="status"></div>
            </div>
        </div>
    )
}

export default SearchCard