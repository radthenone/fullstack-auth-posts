import { PostsData } from 'types/data.tsx';

type PostProps = {
  post: PostsData;
};

const Post = ({ post }: PostProps) => {
  return (
    <div>
      <a href={post.link}>
        <p>{post.title}</p>
        <p>{post.content}</p>
        <p>{post.author}</p>
        <p>{post.date}</p>
      </a>
    </div>
  );
};

export default Post;
