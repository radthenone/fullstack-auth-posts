import { TagType } from 'types/models/tags/tagTypes.tsx';

type PostType = {
  id: number;
  title: string;
  image: string;
  content: string;
  author: string;
  date: string;
  link: string;
  tags: Array<TagType>;
};

type ArrayPostType = Array<PostType>;

export type { PostType, ArrayPostType };
