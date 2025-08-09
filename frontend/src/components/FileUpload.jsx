import React, { useState, useCallback } from "react";
import "./FileUpload.css";

const FileUpload = ({ onFileSelected }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState([]);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles(droppedFiles);
    onFileSelected(droppedFiles);
    setIsDragging(false);
  }, []);

  const handleDragOver = (e) => {
    setIsDragging(true);
    e.preventDefault();
  };

  const handleDragEnter = () => {
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleFileSelect = (e) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  return (
    <div className="upload-container">
      <div
        className={`drop-zone ${isDragging ? "dragging" : ""}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
      >
        {isDragging ? (
          <p className="drag-message">Drop here!</p>
        ) : (
          <>
            <p>Drag and drop files here</p>
            <p className="small-text">or click below</p>
            <input
              type="file"
              multiple
              onChange={handleFileSelect}
              className="file-input"
            />
          </>
        )}
      </div>

      {files.length > 0 && (
        <div className="file-list">
          <h2>Selected Files:</h2>
          <ul>
            {files.map((file, index) => (
              <li key={index}>
                {file.name} ({(file.size / 1024).toFixed(1)} KB)
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
