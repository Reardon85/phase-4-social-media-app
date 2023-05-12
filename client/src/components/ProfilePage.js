import React, { useEffect, useState } from 'react'

import { useParams, useNavigate } from "react-router-dom";
import './styles/ForYou.css';
import "./styles/ProfilePage.css"
import ProfileCard from './ProfileCard'
import ForYouCard from './ForYouCard'
function ProfilePage() {

    const { userId } = useParams();
    const [profileInfo, setProfileInfo] = useState({})

    const [postList, setPostList] = useState([])
    const [amFollowing, setAmFollowing] = useState([false, true])
    const [refreshState, setRefrehState] = useState(false)

    useEffect(() => {
        fetch(`/users/${userId}`)

            .then((r) => {
                if (r.ok) {
                    r.json().then((data) => {
                        setProfileInfo(data['profile_info'])
                        setPostList(data['posts'])
                        console.log(data['posts'])
                        setAmFollowing(data['am_following'])
                        console.log(data)
                    })
                }
            })

    }, [refreshState, userId])


    const post_array = postList.map((post) => (
        <div className="post-container" key={post.id}>
            <ForYouCard {...post} />
        </div>
    ));






    return (
        <div className='profile-page'>

            <ProfileCard profileInfo={profileInfo} amFollowing={amFollowing} setRefrehState={setRefrehState} userId={userId} />
            <div>

                <div className="image-grid">{post_array}</div>;
                    {/* <button className="more-btn" onClick={() => setTotal((total) => total + 21)}>
                        {morePosts ? "MORE POSTS" : "NO MORE POSTS"}
                    </button> */}
                </div>


        </div>
    )
}

export default ProfilePage