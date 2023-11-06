import { TagType } from 'types/models/tagTypes.tsx';

type PostType = {
  id: number;
  title: string;
  image: string;
  content: string;
  author: string;
  date: string;
  link: string;
  tags: TagType[];
};

type PostsResponse = PostType[];

export type { PostType, PostsResponse };
