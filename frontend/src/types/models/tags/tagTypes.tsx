type TagType = {
  id: number;
  name: string;
};

type tagsStateType = {
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  data: ArrayTagType;
  error: string;
};

type ArrayTagType = Array<TagType>;

export type { TagType, ArrayTagType, tagsStateType };
