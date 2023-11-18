import { Routes, Route } from 'react-router-dom';
import Home from 'pages/Screen/Home/Home.tsx';
import Login from 'pages/Login/Login.tsx';
// import RequireAuth from 'features/auth/components/RequireAuth.tsx';
import PostDetail from 'pages/Posts/PostDetail.tsx';
import Posts from 'pages/Posts/Posts.tsx';
import Tags from 'pages/Tags/Tags.tsx';
import TagDetail from 'pages/Tags/TagDetail.tsx';
import { CreateTagForm } from 'pages/Tags/CreateTagForm.tsx';
import { UpdateTagForm } from 'pages/Tags/UpdateTagForm.tsx';
import { DeleteTagForm } from 'pages/Tags/DeleteTagForm.tsx';

export function Router() {
  return (
    <>
      <Routes>
        {/*Public routes*/}

        {/*Screen*/}
        <Route path="/" element={<Home />} />

        {/*Auth*/}
        <Route path="/login" element={<Login />} />
        <Route path="/tags" element={<Tags />} />
        <Route path="/tags/:id" element={<TagDetail />} />
        <Route path="/tags/create" element={<CreateTagForm />} />
        <Route path="/tags/:id/update" element={<UpdateTagForm />} />
        <Route path="/tags/:id/delete" element={<DeleteTagForm />} />
        <Route path="/posts" element={<Posts />} />
        <Route path="/posts/:id" element={<PostDetail />} />
        {/*<Route element={<RequireAuth />}></Route>*/}
      </Routes>
    </>
  );
}
