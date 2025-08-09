import SplitText from "./../components/SplitText";

const Home = () => {
  const handleClick = () => {
    window.location.href = "/upload";
  };

  return (
    <>
      <div className="header">
        <h1 className="header.title noselect">
          {" "}
          <SplitText
            text="Plotify"
            className="header.title"
            delay={100}
            duration={0.6}
            ease="power3.out"
            splitType="chars"
            from={{ opacity: 0, y: 40 }}
            to={{ opacity: 1, y: 0 }}
            threshold={0.1}
            rootMargin="0px"
            textAlign="center"
          />
        </h1>
      </div>
      <div className="holographic-container">
        <div className="holographic-card" onClick={handleClick}>
          <h2 className="noselect">Get started</h2>
        </div>
      </div>
    </>
  );
};

export default Home;
