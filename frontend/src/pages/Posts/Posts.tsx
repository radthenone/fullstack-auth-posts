import { useGetAllPostsQuery } from 'app/services';
import PaginationPosts from 'features/posts/components/PaginationPosts.tsx';
import { Box } from '@mui/material';

const Posts = () => {
  const {
    data: posts = [],
    isLoading: isLoadingPosts,
    isError: isErrorPosts,
    error: errorPosts,
  } = useGetAllPostsQuery();

  if (isLoadingPosts || isErrorPosts) {
    return <div>Loading...</div>;
  }

  if (errorPosts) {
    return <div>Error: {(errorPosts as Error).message}</div>;
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
