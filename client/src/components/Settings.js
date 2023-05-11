import React from 'react';

import "./Settings.css"

function Settings({setUsers, users, setShowForm, showForm}) {
    const updateUser = (event, id) => {
        event.preventDefault();
        const username = event.target.username.value
        const _password_hash = event.target._password_hash.value
        const avatar_url = event.target.avatar_url.value
        const bio = event.target.bio.value
        
       
        fetch(`http://127.0.0.1:5555/orders/${parseInt(customerId)}`,{
          method: 'PATCH',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            username: username,
            _password_hash: _password_hash,
            avatar_url: avatar_url,
            bio: bio
    
          }),
        })
        .then(response => response.json())
        .then (data=> {
          setUsers(users, data)
          setShowForm(!showForm)
        })
      }
  return (
    
        <form onSubmit={updateOrder}>
            <label htmlFor="username">Username:</label>
            <input type="text" id="username" name="username" />
            <label htmlFor="_password_hash">Password:</label>
            <input type="text" id="_password_hash" name="_password_hash"/>
            <label htmlFor="avatar_url">Profile Picture:</label>
            <input type="text" id="avatar_url" name="avatar_url" />
            <label htmlFor="bio">Bio:</label>
            <input type="text" id="bio" name="bio" />
            <label htmlFor="user_id">Name:</label>
            <select id="user" name="user">
              {users.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.name}
                </option>
              ))}
            </select>
            <button type="submit">Update Account</button>
          </form>
          

  )
}

export default Settings;