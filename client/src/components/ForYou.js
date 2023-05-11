import React, { useState, useEffect } from 'react';
import './styles/ForYou.css';
import ForYouCard from './ForYouCard';

function ForYou() {
    const [posts, setPosts] = useState([]);
    const [total, setTotal] = useState(21);
    const [morePosts, setMorePosts] = useState(true);

    useEffect(() => {
        fetch(`/homeforyou/${total}`)
            .then((r) => {
                if (r.ok) {
                    r.json().then((data) => {
                        setPosts(data.posts);
                        setMorePosts(data.more_posts);
                    });
                }
            });
    }, [total]);

    const post_array = posts.map((post) => (
        <div className="post-container" key={post.id}>
            <ForYouCard {...post} />
        </div>
    ));

    return (
        <div>

            <div className="image-grid">{post_array}</div>;
            <button className="more-btn" onClick={() => setTotal((total) => total + 21)}>
                {morePosts ? "MORE POSTS" : "NO MORE POSTS"}
            </button>
        </div>
    )
}

export default ForYou;
