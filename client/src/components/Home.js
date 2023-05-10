import React, { useEffect, useState } from "react"
import "./styles/Home.css"
import Post from "./Post"
function Home() {

    const [posts, setPosts] = useState([])

    useEffect(() => {

        fetch('/posts')
            .then((r) => {
                if (r.ok) {
                    r.json().then((data) => {

                        setPosts(data)
                    })
                }
            })
    }, [])


    const post_array = posts.length > 0 ? posts.map((post) => {

        return <Post key={post.id} {...post} />
    }) : <></>

    return (
        <div class="card">
            {post_array}
        </div>
    )
}

export default Home
