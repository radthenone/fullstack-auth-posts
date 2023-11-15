import { TagType } from 'types';

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

type postStateType = {
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  data: PostType;
  error: string;
};

type postActionType = {
  type: string;
  payload: PostType | string;
};

type postsStateType = {
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  data: ArrayPostType;
  error: string;
};

type postsActionType =
  | { type: string; payload: ArrayPostType[] }
  | { type: string; payload: ArrayPostType }
  | { type: string; payload: string };

type ArrayPostType = Array<PostType>;

export type {
  PostType,
  ArrayPostType,
  postsStateType,
  postStateType,
  postsActionType,
  postActionType,
};
