import React, { useEffect, useState } from 'react'
import {useParams} from "react-router-dom";
import "./styles/ProfilePage.css"
import ProfileCard from './ProfileCard'
import ForYouCard from './ForYouCard'
function ProfilePage() {

    const {userId} = useParams();
    const [profileInfo, setProfileInfo] = useState({})
    const[postList, setPostList] = useState([])
    const [myProfile, setMyProfile] = useState(false)





    useEffect(() => {

        fetch(`/users/${userId}`)
        .then((r) => {
            if (r.ok){
                r.json().then((data) =>{ 
                    setProfileInfo(data['profile_info'])
                    setPostList(data['posts'])
                    setMyProfile(data['my_profile'])
                    return
                })
            }
        })


    }, [])


    return (
        <div className='profile-page'>
            <ProfileCard profileInfo={profileInfo} />

        </div>
    )
}

export default ProfilePage