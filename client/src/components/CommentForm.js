import React, { useState, useEffect } from 'react';
import "./styles/CommentForm.css";
import Comment from './Comment';


const CommentForm = ({ postId }) => {
  const [comment, setComment] = useState('');
  const [commentList, setCommentList] = useState([])


  useEffect(() => {

    fetch(`/comments/${postId}`)
      .then((r) => r.json())
      .then((d) => setCommentList(d))


  }, [postId])


  const comment_array = commentList.map((c) => {
    return <Comment key={c.id} username={c.username} avatar={c.avatar_url} timestamp={c.date_posted} content={c.content} />
  })

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you would handle the comment submission, for instance, by calling an API endpoint.
    console.log(comment);
    const comment_info = {
      postId: postId,
      text: comment,
    }

    fetch('/comments', {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(comment_info)
    }).then((r) => r.json())
      .then((d) => setCommentList((commentList) => commentList.concat(d)))


    setComment('');
  }



  //   const commentArray = comments.map((comment) => {
  //     <Comment key={comment.id} username={comment.username} timestamp={comment.datePosted} />
  //   })


  return (
    <>
      {comment_array}
      <form className="comment-form" onSubmit={handleSubmit}>
        <textarea
          className="comment-input"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Write your comment..."
        />
        <button className="com-btn" type="submit">Submit</button>
      </form>
    </>
  );
};

export default CommentForm;