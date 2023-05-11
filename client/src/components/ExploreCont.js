import React from "react";
import ExploreCard from './ExploreCard';

function ExploreCont({ posts, onUpdatePost }) {
  const postCards = posts.map((post) => (
    <ExploreCard
      key={post.id}
      post={post}
      onUpdatePost={onUpdatePost}
      />
      ));
      
  return <div id="post-collection">{postCards}</div>;
    }
    
export default ExploreCont;
    // image={post.image}
    // likes={post.likes}