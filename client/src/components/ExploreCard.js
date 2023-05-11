import React from 'react'
// import Explore from '../explore'
// import postsData from "../explore";

// const Front = ({image }) => {
//     return (
//         <div>
//             <img src={ image } alt='photo'/>
//         </div>
//     )
// }

// const Back = ({ posts }) => {
    
//     return (
//         <div>
//             <h1>{ posts.username }</h1>
//             <h3>{ posts.caption }</h3>
//             <h2>{ posts.likes } kilos</h2>
//         </div>
//     )
// }

// const [ showFront, setShowFront ] = useState( false )
// const toggleFront = () => setShowFront( showFront => !showFront )

function ExploreCard({ post, onUpdatePost }){
    const { id, username, image, likes } = post;


    function handleLikeClick() {
        const updateObj = {
          likes: post.likes + 1,
        };
    
        fetch(`http://localhost:3001/posts/${id}`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(updateObj),
        })
          .then((r) => r.json())
          .then(onUpdatePost);
      }
    

    return (
        // <div onClick={ toggleFront } 
        <div className="card">
        <h2>{username}</h2>
        <img src={image} alt={image} className="post-image" />
        <p>{likes} Likes </p>
        <button className="like-btn" onClick={handleLikeClick}>
          Like {"<3"}
        </button>
      </div>
    )
}

export default ExploreCard
