// import DragNDrop from "./../components/DragNDrop";
// import { FileUploader } from "react-drag-drop-files";
import { FiUpload } from "react-icons/fi";
import React, { useState, useEffect } from "react";
import FileUpload from "./../components/FileUpload";
import Header from "./../components/Header";

const Upload = () => {
  const [files, setFiles] = useState([]);
  const handleFileSelected = (file) => {
    setFiles(file);
  };
  const [data, setData] = useState(null);

  const handleUploadClick = async () => {
    if (files.length === 0) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", files[0]);
    // files.forEach((file) => {
    //   formData.append("files[]", file);
    // });

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      const result = await response.json();
      console.log("Server response:", result);
      alert("Upload successful!");
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed!");
    }

    window.location.href = "/insights";
  };
  return (
    <>
      <Header />
      <h2 className="uploadtext">Upload a JSON file, or a zip of JSONs</h2>
      <FileUpload onFileSelected={handleFileSelected} />
      <button className="upload-button" onClick={handleUploadClick}>
        <FiUpload />
        Upload
      </button>
    </>
  );
};

export default Upload;
