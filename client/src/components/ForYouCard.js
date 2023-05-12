import React from 'react';
import './styles/ForYouCard.css';
import { Link } from 'react-router-dom';




function ForYouCard({ image, comment_count, like_count, id}) {

    return (
    <Link to={`/posts/${id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
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
    </Link>
    );
}

export default ForYouCard;