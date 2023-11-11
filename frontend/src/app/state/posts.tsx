import { PostType } from 'types/models/posts/postTypes.tsx';

const PostState = {
  value: {
    id: 0,
    title: '',
    image: '',
    content: '',
    author: '',
    date: '',
    link: '',
    tags: [],
  } as PostType,
};

export { PostState };
