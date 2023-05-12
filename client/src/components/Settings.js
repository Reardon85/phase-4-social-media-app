import React, { useState, useEffect } from 'react';
import "./styles/Settings.css"

function Settings() {

  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      console.log('No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
      await fetch('/upload_image', {
        method: 'POST',
        body: formData,
      });
    } catch (error) {
      console.error('Error occurred during image upload:', error);
    }
  };



  return (
    <div class="upload-container">
      <h1>Upload an Image</h1>
      <input type="file" onChange={handleFileChange} accept="image/*" />
      {file && (
        <div>
          <img src={URL.createObjectURL(file)} alt="Selected file" />
        </div>
      )}
      <h2>Name:</h2>
      <input type="text" placeholder="Add a caption" />
      <h2>Bio:</h2>
      <input type="text" placeholder="Add a caption" />
      <button onClick={handleSubmit}>Upload</button>
    </div>
  );
}
export default Settings;
