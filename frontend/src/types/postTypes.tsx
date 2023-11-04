import { TagType } from 'types/tagTypes';

type PostType = {
  id: number;
  title: string;
  content: string;
  author: string;
  date: string;
  link: string;
  tags: TagType[];
};

type PostsResponse = PostType[];

export type { PostType, PostsResponse };
