import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import CommentForm from './CommentForm';
import "./styles/PostCard.css";

function PostCard() {

    const [likes, setlikes] = useState(0)
    const [like, setlike] = useState(false)
    const {postId} = useParams()
    const [comments, setComments] = useState([])
    const [postInfo, setPostInfo] = useState([])

    useEffect( ()=>{

        fetch(`/posts/${postId}`)
        .then((r) =>{
            if(r.ok){
                r.json().then((d) =>{
       

                    setlikes(d.like_count)
                    setlike(d.liked)
                    setPostInfo([d.id, d.avatar_url, d.username, d.user_id, d.image, d.content, d.date_posted])

                })
            }
        })



    },[])
    console.log(comments)


    let semaphore = true

    const handleLike = () => {

        if (semaphore) {
            semaphore = false
            if (like) {
                fetch(`/likes/${postId}`, {
                    method: "DELETE",
                }
                ).then((r) => {
                    if (r.ok) {
                        console.log("deleting")
                        setlikes((likes) => likes - 1)
                        setlike((like) => !like)

                    }
                })
            }
            else {
                fetch(`/likes/${postId}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: {}
                }
                ).then((r) => {
                    if (r.ok) {
                        console.log("deleting")
                        setlike((like) => !like)
                        setlikes((likes) => likes + 1)

                    }
                })
            }
            semaphore = true
            console.log('postinfo')
            console.log(postInfo)
        }
    }
   
    return (

        <div className="post-container">

            <div className="post-card">
                <div className="post-header">
                    <Link to={`/profile/${postInfo[3]}`} ><img src={postInfo[1]} alt="User Profile" className="user-profile-photo" /></Link>
                    <Link to={`/profile/${postInfo[3]}`} style={{ textDecoration: 'none', color: 'inherit' }}><h2 className="user-name">{postInfo[2]}</h2></Link>
                </div>
                <img src={postInfo[4]} alt="Post" className="post-image" />
                <div className="post-footer">


                    <h2 className='likes-title'>Likes: {likes}</h2>
                    <button onClick={handleLike} class={like ? "like-btn" : "like-btn"}>
                        <svg viewBox="0 0 17.503 15.625" height="20.625" width="20.503" xmlns="http://www.w3.org/2000/svg" class={like ? "iconn" : "icon"}>

                            <path transform="translate(0 0)" d="M8.752,15.625h0L1.383,8.162a4.824,4.824,0,0,1,0-6.762,4.679,4.679,0,0,1,6.674,0l.694.7.694-.7a4.678,4.678,0,0,1,6.675,0,4.825,4.825,0,0,1,0,6.762L8.752,15.624ZM4.72,1.25A3.442,3.442,0,0,0,2.277,2.275a3.562,3.562,0,0,0,0,5l6.475,6.556,6.475-6.556a3.563,3.563,0,0,0,0-5A3.443,3.443,0,0,0,12.786,1.25h-.01a3.415,3.415,0,0,0-2.443,1.038L8.752,3.9,7.164,2.275A3.442,3.442,0,0,0,4.72,1.25Z" id="Fill"></path>
                        </svg>
                    </button>
                    <h3 className='date-title'>{postInfo['date_posted']}</h3>
                    {/* <button className="comment-btn"><i className="fas fa-comment"></i> Comment</button> */}

                </div>
            </div>    
            <div className="comment-form-container">
                <CommentForm postId={postId}/>
            </div>

        </div>

    );
}

export default PostCard;