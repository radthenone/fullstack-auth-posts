import { Routes, Route } from 'react-router-dom';
import Home from 'pages/Screen/Home/Home.tsx';
import Login from 'pages/Login/Login.tsx';

function Router() {
  return (
    <>
      <Routes>
        {/*Screen*/}
        <Route path="/" element={<Home />} />

        {/*Auth*/}
        <Route path="/login" element={<Login />} />
      </Routes>
    </>
  );
}

export default Router;
