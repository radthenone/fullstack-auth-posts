import { Routes, Route } from 'react-router-dom';
import Home from 'pages/Screen/Home/Home.tsx';
import Login from 'pages/Login/Login.tsx';
import RequireAuth from 'features/auth/components/RequireAuth.tsx';
import PostDetail from 'pages/Posts/PostDetail.tsx';

export function Router() {
  return (
    <>
      <Routes>
        {/*Public routes*/}

        {/*Screen*/}
        <Route path="/" element={<Home />} />

        {/*Auth*/}
        <Route path="/login" element={<Login />} />
        <Route path="/posts/:id" element={<PostDetail />} />
        <Route element={<RequireAuth />}></Route>
      </Routes>
    </>
  );
}
