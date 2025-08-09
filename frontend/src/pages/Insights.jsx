import React, { useState, useEffect } from "react";
import Header from "./../components/Header";
import InsightBox from "./../components/InsightBox";

const Insights = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/get_insights", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error("Error fetching:", err));
  }, []);

  return (
    <>
      <Header />
      <style>{`
        .insight-box {
          transition: transform 0.2s cubic-bezier(.4,0,.2,1), box-shadow 0.2s;
        }
        .insight-box:hover {
          transform: scale(1.07);
          box-shadow: 0 8px 32px rgba(0,0,0,0.22);
        }
      `}</style>
      <div style={{ padding: "2rem" }}>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "2.5rem",
            flexWrap: "wrap",
            marginTop: "10rem",
          }}
        >
          {data ? (
            <>
              <InsightBox
                label="Your most played song"
                value={data["topsong"]["songname"]}
                gradient="linear-gradient(90deg, #ff8c00, #ff0080)"
              />
              <InsightBox
                label="Your favourite singer"
                value={data["topsinger"]["artistname"]}
                gradient="linear-gradient(90deg, #00c6ff, #0072ff)"
              />
              <InsightBox
                label="Total time listened"
                value={data["totalhours"]}
                gradient="linear-gradient(90deg, #43e97b, #38f9d7)"
              />
              <InsightBox
                label="You are a"
                value={data["timeofday"]}
                gradient="linear-gradient(90deg, #f7971e, #ffd200)"
              />
            </>
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>
    </>
  );
};

export default Insights;
