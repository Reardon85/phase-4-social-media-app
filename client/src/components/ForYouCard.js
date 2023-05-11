import React from 'react';
import './styles/ForYouCard.css';




function ForYouCard({ image, comment_count, like_count }) {

    return (
        <div className="image-grid">
            <div className="image-container">
                <img src={image} alt="Placeholder" />
                <div className="image-overlay">
                    <div className="image-overlay-text">
                        🤍 {like_count}
                        <span>💬 {comment_count}</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ForYouCard;
