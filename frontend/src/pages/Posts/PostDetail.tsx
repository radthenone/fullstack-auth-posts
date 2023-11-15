import PostCard from 'pages/Posts/PostCard.tsx';
import { useGetPostQuery } from 'app/posts/hooks';

const PostDetail = () => {
  const post = useGetPostQuery();

  return (
    <>
      <PostCard key={post?.id} postId={post?.id} />
    </>
  );
};

export default PostDetail;
