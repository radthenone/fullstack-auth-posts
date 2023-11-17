type TagType = {
  id: number;
  name: string;
};

type tagsStateType = {
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  isCreated: boolean;
  data: TagType[];
  error: string;
};

type tagStateType = {
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  isUpdated: boolean;
  isDeleted: boolean;
  data: TagType | null;
  error: string;
};

type ArrayTagType = Array<TagType>;

export type { TagType, ArrayTagType, tagsStateType, tagStateType };
