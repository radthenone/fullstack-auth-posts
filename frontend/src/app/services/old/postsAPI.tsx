import { api } from 'app/services/old/index.tsx';
import type { PostType, ArrayPostType } from 'types';

export const postsApi = api.injectEndpoints({
  endpoints: (build) => ({
    getAllPosts: build.query<ArrayPostType, void>({
      query: () => ({ url: 'posts' }),
      providesTags: ['Posts'],
    }),
    getPost: build.query<PostType, number>({
      query: (id) => ({ url: `posts/${id}` }),
      providesTags: (post) => [{ type: 'Posts', id: post?.id }],
    }),
    addPost: build.mutation<PostType, Partial<PostType>>({
      query(body) {
        return {
          url: `posts`,
          method: 'POST',
          body,
        };
      },
      invalidatesTags: ['Posts'],
    }),
    updatePost: build.mutation<PostType, Partial<PostType>>({
      query(data) {
        const { id, ...body } = data;
        return {
          url: `posts/${id}`,
          method: 'PUT',
          body,
        };
      },
      invalidatesTags: (post) => [{ type: 'Posts', id: post?.id }],
    }),
    deletePost: build.mutation<{ success: boolean; id: number }, number>({
      query(id) {
        return {
          url: `posts/${id}`,
          method: 'DELETE',
        };
      },
      invalidatesTags: (post) => [{ type: 'Posts', id: post?.id }],
    }),
  }),
});

export const {
  useGetAllPostsQuery,
  useAddPostMutation,
  useGetPostQuery,
  useUpdatePostMutation,
  useDeletePostMutation,
} = postsApi;
