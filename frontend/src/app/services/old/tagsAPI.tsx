import { api } from 'app/services/old/index.tsx';
import type { TagType } from '@/types';

export const tagsAPI = api.injectEndpoints({
  endpoints: (build) => ({
    getAllTags: build.query<TagType[], void>({
      query: () => ({
        url: 'tags',
        method: 'GET',
      }),
    }),
    getTag: build.query<TagType, string>({
      query: (id) => ({
        url: `tags/${id}`,
        method: 'GET',
        params: {
          id,
        },
      }),
    }),
  }),
});

export const { useGetAllTagsQuery, useGetTagQuery } = tagsAPI;
