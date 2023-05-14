import React, { useState, useEffect } from 'react';
import "./styles/Settings.css"

function Settings() {




  const [file, setFile] = useState(null);
  const [email, setEmail] = useState('');
  const [bio, setBio] = useState('');
  const [profilePic, setProfilePic] = useState(null);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');




  useEffect(()=> {

    fetch('/update-profile')
    .then((r)=> r.json())
    .then((d)=> {
      setBio(d.bio)
      setEmail(d.email)
      setProfilePic(d.avatar_url)
    })


  },[])
  console.log(profilePic)

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    if (file === null) {
      formData.append('fileExists', 'false')
      console.log(file)
    } else {
      formData.append('fileExists', 'true')
    }
    if(currentPassword === '' || newPassword === '')
    {
      formData.append('currentPassword', 'null')
      formData.append('newPassword', 'null')
    } else{
      formData.append('currentPassword', currentPassword)
      formData.append('newPassword', newPassword)
    }
    formData.append('image', file);
    formData.append('bio', bio)
    formData.append('email', email)


    try {
      await fetch('/update-profile', {
        method: 'PATCH',
        body: formData,
      });
    } catch (error) {
      console.error('Error occurred during image upload:', error);
    }
    setFile(null)
    setCurrentPassword('')
    setNewPassword('')
  };

  console.log(currentPassword)

  const handleNewPChange = (event) => {
    console.log(event.target.value)
    setNewPassword((bio) => event.target.value)
  }

  const handleCurrentPChange = (event) => {
    console.log(event.target.value)
    setCurrentPassword((bio) => event.target.value)
  }

  const handleBioChange = (event) => {
    console.log(event.target.value)
    setBio((bio) => event.target.value)
  }

  const handleEmailChange = (event) => {
    console.log(event.target.value)
    setEmail((email) => event.target.value)
  }



  return (
    <div class="upload-container">
      <img></img>
      <h4 className='pi' >Change Profile Image</h4>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      {file && (
        <div>
          <img className='preview-image' src={file ? URL.createObjectURL(file) : profilePic} alt="Selected file" />
        </div>
      )}
      <h4>Current Password:</h4>
      <input onChange={handleCurrentPChange} type="password" value={currentPassword} autocomplete="new-password" readonly 
onfocus="this.removeAttribute('readonly');" />
      <h4>New Password:</h4>
      <input onChange={handleNewPChange} type="password" value={newPassword} autocomplete="new-password" readonly 
onfocus="this.removeAttribute('readonly');" />
      <h4>Email:</h4>
      <input onChange={handleEmailChange} type="text" value={email} />
      <h4>Bio:</h4>
      <input onChange={handleBioChange} type="text" value={bio} />
      <button onClick={handleSubmit}>Update</button>
    </div>
  );
}
export default Settings;
