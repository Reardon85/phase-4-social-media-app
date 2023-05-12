import React, { useState, useRef } from 'react';
import "./styles/Create.css"

function Create() {


  const [file, setFile] = useState(null);
  const [caption, setCaption] = useState(null)

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
  };

  const handleCaptionChange = (event) => {
    console.log(event.target.value)
    setCaption((caption)=> event.target.value)
  }
  
  const handleSubmit = (event) => {
    event.preventDefault();

    if (!file) {
      console.log('No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('image', file);
    formData.append('content', caption)
    console.log(formData)

    try {
       fetch('/create-post', {
        method: 'POST',
        body: formData,
      })
      .then((r) => r.json())
      .then((d) => {
        setFile(null)
        setCaption(null);
      })
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
      <input type="text" onChange={handleCaptionChange} placeholder="Add a caption"  value={caption}/>
      <button onClick={handleSubmit}>Upload</button>
    </div>
  );
}

export default Create;