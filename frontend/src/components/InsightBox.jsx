import React from "react";

const InsightBox = ({ label, value, gradient }) => (
  <div
    className="insight-box"
    style={{
      background: "#23272f",
      borderRadius: "16px",
      boxShadow: "0 4px 16px rgba(0,0,0,0.15)",
      padding: "2.5rem 2rem",
      minWidth: "260px",
      textAlign: "center",
      color: "#fff",
    }}
  >
    <div
      style={{
        fontSize: "1.1rem",
        marginBottom: "0.7rem",
        color: "#bdbdbd",
      }}
    >
      {label}
    </div>
    <div
      style={{
        fontWeight: "bold",
        fontSize: "2rem",
        background: gradient,
        WebkitBackgroundClip: "text",
        WebkitTextFillColor: "transparent",
      }}
    >
      {value}
    </div>
  </div>
);

export default InsightBox;
