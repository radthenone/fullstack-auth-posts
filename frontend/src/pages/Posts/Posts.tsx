import { useGetPostsQuery } from 'app/posts/hooks';
import PaginationPosts from 'features/posts/components/PaginationPosts.tsx';
import { Box } from '@mui/material';

const Posts = () => {
  const {
    data: posts = [],
    isLoading: isLoadingPosts,
    isError: isErrorPosts,
    error: errorPosts,
  } = useGetPostsQuery();

  if (isLoadingPosts || isErrorPosts) {
    return <div>Loading...</div>;
  }

  if (isErrorPosts) {
    return <div>Error: {errorPosts}</div>;
  }

  return (
    <>
      <Box sx={{ p: 3 }}>
        <PaginationPosts data={posts} start={1} end={15} count={15} />
      </Box>
    </>
  );
};

export default Posts;
