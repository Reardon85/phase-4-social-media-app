import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import Message from './Message'
import "./styles/MessageCenter.css";

function MessageCenter() {

    const [likes, setlikes] = useState(0)
    const [like, setlike] = useState(false)
    const { postId } = useParams()
    const navigate = useNavigate()
    const [postInfo, setPostInfo] = useState([])

    useEffect(() => {

        fetch(`/posts/${postId}`)
            .then((r) => {
                if (r.ok) {
                    r.json().then((d) => {


                        setlikes(d.like_count)
                        setlike(d.liked)
                        setPostInfo([d.id, d.avatar_url, d.username, d.user_id, d.image, d.content, d.date_posted, d.my_post])

                    })
                }
            })



    }, [postId])
  



    const handleDelete = () => {

        fetch(`/posts/${postId}`, {
            method: "DELETE",
        })
        .then((r) => {
            if (r.ok){
                navigate('/')
            }
        })
    }


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

        }
    }

    return (

        <div className="post-container">

            <div className="discussion-card">

                <div className='postcard-image-container'> 
                </div>
                
            </div>


            <div className="message-form-container">
          
              <form className="comment-form" onSubmit={''}>
                <textarea
                className="comment-input"
                value={''}
                onChange={(e) => ''}
                placeholder="Write your comment..."
                />
                <button className="com-btn" type="submit">Submit</button>
              </form>

            </div>

        </div>

    );
}

export default MessageCenter;