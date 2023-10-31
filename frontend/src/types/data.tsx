type TagsData = {
  id: number;
  name: string;
};

type PostsData = {
  id: number;
  title: string;
  content: string;
  author: string;
  date: string;
  link: string;
  tags: TagsData[];
};

export type { TagsData, PostsData };
