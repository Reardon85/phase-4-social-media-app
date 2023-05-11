import React, { useEffect, useState } from 'react'

import {useParams, useNavigate } from "react-router-dom";

import "./styles/ProfilePage.css"
import ProfileCard from './ProfileCard'
import ForYouCard from './ForYouCard'
function ProfilePage() {

    const { userId } = useParams();
    const [profileInfo, setProfileInfo] = useState({})

    const[postList, setPostList] = useState([])
    const [amFollowing, setAmFollowing] = useState([false, true])
    const [refreshState, setRefrehState] = useState(false)


    const navigate = useNavigate()

    console.log(useParams())


    useEffect(() => {

        console.log("Hello?")

        fetch(`/users/${userId}`)

        .then((r) => {
            if (r.ok){
                r.json().then((data) =>{ 
                    setProfileInfo(data['profile_info'])
                    setPostList(data['posts'])
                    setAmFollowing(data['am_following'])
                    console.log(data)
                })
            }
        })



    }, [refreshState])

    function handleFollow(following){
        console.log("workings")
        
        if (following){
            fetch(`/follow/${userId}`, {
                method: 'DELETE',
            }).then((r) => {
                setRefrehState((refreshState) => !refreshState)
            } )
        }
        else{
            fetch('/follow', {
                method: "POST",
                headers: {
                    'Content-Type':'application/json'
                },
                body: JSON.stringify({userId: userId}) 
            
            })
            .then((r) => {
                if (r.ok){
                    setRefrehState((refreshState) => !refreshState)
                }
            })


        }

    }


    
    function handleSettings(){

        navigate("/settings")
    }





    return (
        <div className='profile-page'>

            <ProfileCard profileInfo={profileInfo} amFollowing={amFollowing} handleFollow={handleFollow} handleSettings={handleSettings} />


        </div>
    )
}

export default ProfilePage