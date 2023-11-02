import { createApi } from '@reduxjs/toolkit/query/react';
import axiosBaseQuery from 'app/axiosBaseQuery';
import { TagsData } from 'types/data.tsx';

const baseUrl = `${process.env.TEST_URL}/tags`;

const tagsAPI = createApi({
  reducerPath: 'api',
  baseQuery: axiosBaseQuery({ baseUrl: baseUrl }),
  tagTypes: ['Tags'],
  endpoints: (build) => ({
    getTags: build.query<TagsData[], void>({
      query: () => ({
        url: 'tags',
        method: 'GET',
      }),
    }),
    getTagById: build.query<TagsData, string>({
      query: (id) => ({
        url: `tags/${id}`,
        method: 'GET',
      }),
    }),
    createTag: build.mutation<TagsData, TagsData>({
      query: (tag) => ({
        url: 'tags',
        method: 'POST',
        body: tag,
      }),
    }),
    updateTag: build.mutation<TagsData, TagsData>({
      query: (tag) => ({
        url: `tags/${tag.id}`,
        method: 'PUT',
        body: tag,
      }),
    }),
    deleteTag: build.mutation<TagsData, string>({
      query: (id) => ({
        url: `tags/${id}`,
        method: 'DELETE',
      }),
    }),
  }),
});

export const {
  useGetTagsQuery,
  useGetTagByIdQuery,
  useCreateTagMutation,
  useUpdateTagMutation,
  useDeleteTagMutation,
} = tagsAPI;
