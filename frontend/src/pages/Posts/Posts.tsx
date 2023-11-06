import { useGetAllPostsQuery } from 'app/services';

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
      <div>
        {posts.map((post) => (
          <div key={post.id}>
            <a href={post.link}>
              <p>{post.title}</p>
              <p>{post.content}</p>
              <p>{post.author}</p>
              <p>{post.date}</p>
            </a>
          </div>
        ))}
      </div>
    </>
  );
};

export default Posts;
