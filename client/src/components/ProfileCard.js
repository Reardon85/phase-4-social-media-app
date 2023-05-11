import React, { useEffect } from 'react'
import "./styles/ProfileCard.css"


function ProfileCard({profileInfo, amFollowing, handleFollow, handleSettings}) {

    // useEffect()




    return (
        <main class="pf-container">
            <div class="pf-card">
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
                        <button onClick={() => {handleFollow(true)}} class="card__action__button card__action--message">Following</button>
                        :
                        <button onClick={() => {handleFollow(false)}} class="card__action__button card__action--message">Follow</button>
                    }
                </div>
            </div>
        </main>
    );
}

export default ProfileCard;

