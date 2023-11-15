import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { postsState } from 'app/posts/state';
import { postsStateType, ArrayPostType } from 'types';

const initialState: postsStateType = postsState;

export const posts = createSlice({
  name: 'posts',
  initialState,
  reducers: {
    getPostsLoading: (state) => {
      return {
        ...state,
        isLoading: true,
        isSuccess: false,
        isError: false,
        data: [],
      };
    },
    getPostsSuccess: (state, action: PayloadAction<ArrayPostType>) => {
      return {
        ...state,
        isLoading: false,
        isSuccess: true,
        isError: false,
        data: action.payload,
      };
    },
    getPostsFailure: (state, action: PayloadAction<string>) => {
      return {
        ...state,
        isLoading: false,
        isSuccess: false,
        isError: true,
        error: action.payload,
      };
    },
  },
});

export const { getPostsLoading, getPostsSuccess, getPostsFailure } = posts.actions;
