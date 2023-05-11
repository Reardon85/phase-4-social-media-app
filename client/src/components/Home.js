import React, { useEffect, useState } from "react"
import "./styles/Home.css"
import Post from "./Post"
function Home({setRefreshState, refreshState}) {

    const [posts, setPosts] = useState([])
    const [total, setTotal] = useState(5)
    const [morePosts, setMorePosts] = useState(true)

    useEffect(() => {

        fetch(`/home/${total}`)
            .then((r) => {
                if (r.ok) {
                    r.json().then((data) => {

                        setPosts(data.posts)
                        setMorePosts(data.more_posts)
                    })
                }
            })
    }, [total])




    const post_array =  posts.map((post) => (
        <div className="post-container" key={post.id}>
          <Post {...post} />
        </div>
      ))
    

    return (
        <div className="home-container">
          <div className="card">
            {post_array}
          </div>
          <button className="more-btn" onClick={() => setTotal((total) => total + 5)}>
            {morePosts ?  "MORE POSTS" : "NO MORE POSTS" }
          </button>
        </div>
      )
    }

export default Home
