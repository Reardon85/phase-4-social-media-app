import React from 'react'
import "./styles/ProfileCard.css"

function ProfileCard() {
    return (

        <div class="post-card">
            <div class="post-infos">
                <div class="post-image"></div>
                <div class="post-info">
                    <div>
                        <p class="post-name">
                            John Doe
                        </p>
                        <p class="post-function">
                            Front-end dev
                        </p>
                    </div>
                    <div class="post-stats">
                        <p class="post-flex flex-col">
                            Articles
                            <span class="post-state-value">
                                34
                            </span>
                        </p>
                        <p class="post-flex">
                            Followers
                            <span class="post-state-value">
                                455
                            </span>
                        </p>

                    </div>
                </div>
            </div>
            <button class="post-request" type="button">
                Add friend
            </button>
        </div>

    )
}

export default ProfileCard