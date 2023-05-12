import React, { useEffect } from 'react'
import { useNavigate } from "react-router-dom";

import "./styles/ProfileCard.css"


function ProfileCard({ profileInfo, amFollowing, setRefrehState, userId}) {
    // useEffect()
    const navigate = useNavigate()
    
    function handleSettings(){ 
        navigate("/settings")
    }

    function handleFollow(following) {
        if (following) {
            fetch(`/follow/${userId}`, {
                method: 'DELETE',
            }).then((r) => {
                setRefrehState((refreshState) => !refreshState)
            })
        }
        else {
            fetch('/follow', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ userId: userId })

            })
                .then((r) => {
                    if (r.ok) {
                        setRefrehState((refreshState) => !refreshState)
                    }
                })
        }
    }





    return (
        <main class="pf-container">
            <div class={profileInfo.active ? "pf-card": "pf-card-offline"}>
                <img src={profileInfo.avatar_url} alt="User image" class="card__image" />
                <div class="card__text">
                    <h2>{profileInfo.username}</h2>
                    <p>{profileInfo.bio}</p>
                </div>
                <ul class="card__info">
                    <li>
                        <span class="card__info__stats">{profileInfo.posts}</span>
                        <span>posts</span>
                    </li>
                    <li>
                        <span class="card__info__stats">{profileInfo.followers}</span>
                        <span>followers</span>
                    </li>
                    <li>
                        <span class="card__info__stats">{profileInfo.following}</span>
                        <span>following</span>
                    </li>
                </ul>
                <div class="card__action">
                    {/* <button class="card__action__button card__action--follow">follow</button> */}
                    {amFollowing[0]
                        ?
                        <button onClick={handleSettings} class="card__action__button card__action--message">Settings</button>
                        :
                        amFollowing[1]
                            ?
                            <button onClick={() => { handleFollow(true) }} class="card__action__button card__action--message">Unfollow</button>
                            :
                            <button onClick={() => { handleFollow(false) }} class="card__action__button card__action--message">Follow</button>
                    }
                </div>
            </div>
        </main>
    );
}

export default ProfileCard;

