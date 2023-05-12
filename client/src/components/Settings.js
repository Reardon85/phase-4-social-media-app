import React, { useState, useEffect } from 'react';
import "./styles/Settings.css"

function Settings() {

  const [file, setFile] = useState(null);
  const [email, setEmail] = useState('');
  const [bio, setBio] = useState('');


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
  };

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
      <h2 className='pi' >Change Profile Image</h2>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      {file && (
        <div>
          <img className='preview-image' src={URL.createObjectURL(file)} alt="Selected file" />
        </div>
      )}
      <h2>Email:</h2>
      <input onChange={handleEmailChange} type="text" value={email} />
      <h2>Bio:</h2>
      <input onChange={handleBioChange} type="text" value={bio} />
      <button onClick={handleSubmit}>Update</button>
    </div>
  );
}
export default Settings;
