import { PostType } from 'types/postTypes';
import { useGetPostQuery } from 'app/services/postsAPI';

const postState: PostType = {
  id: 0,
  link: '',
  title: '',
  content: '',
  author: '',
  date: '',
  tags: [],
};

const Post = () => {
  const {
    data: { link, title, content, author, date } = postState,
    isLoading,
    isError,
    error,
  } = useGetPostQuery();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div>
      <a href={link}>
        <p>{title}</p>
        <p>{content}</p>
        <p>{author}</p>
        <p>{date}</p>
      </a>
    </div>
  );
};

export default Post;
