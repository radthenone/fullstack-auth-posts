import { TagType } from 'types';

const tagsState = {
  data: [],
  error: '',
  isLoading: false,
  isSuccess: false,
  isError: false,
  isCreated: false,
};

const tagState = {
  data: {
    id: 0,
    name: '',
  } as TagType | null,
  error: '' as string,
  isLoading: false,
  isSuccess: false,
  isError: false,
  isUpdated: false,
  isDeleted: false,
};

export { tagsState, tagState };
