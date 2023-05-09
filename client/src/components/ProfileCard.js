import React from 'react'
import "./styles/ProfileCard.css"


function ProfileCard() {
    return (
        <main class="pf-container">
            <div class="pf-card">
                <img src="https://res.cloudinary.com/alexandracaulea/image/upload/v1582179610/user_fckc9f.jpg" alt="User image" class="card__image" />
                <div class="card__text">
                    <h2>Alexandra Caulea</h2>
                    <p>I enjoy drinking a cup of coffee every day</p>
                </div>
                <ul class="card__info">
                    <li>
                        <span class="card__info__stats">172</span>
                        <span>posts</span>
                    </li>
                    <li>
                        <span class="card__info__stats">47</span>
                        <span>followers</span>
                    </li>
                    <li>
                        <span class="card__info__stats">20</span>
                        <span>following</span>
                    </li>
                </ul>
                <div class="card__action">
                    {/* <button class="card__action__button card__action--follow">follow</button> */}
                    <button class="card__action__button card__action--message">Settings</button>
                </div>
            </div>
        </main>
    );
}

export default ProfileCard;

