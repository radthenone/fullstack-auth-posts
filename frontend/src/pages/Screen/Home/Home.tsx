import MainTags from 'pages/Tags/MainTags.tsx';
function Home() {
  return (
    <>
      <p>Homepage</p>
      <p>{process.env.TEST_URL}</p>
      <MainTags />
    </>
  );
}

export default Home;
