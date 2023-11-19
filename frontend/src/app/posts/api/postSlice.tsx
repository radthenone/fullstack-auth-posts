import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { postsState } from 'app/posts/state';
import { postsStateType, PostType } from 'types';

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
    getPostsSuccess: (state, action: PayloadAction<PostType[]>) => {
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
    addPostSuccess: (state, action: PayloadAction<PostType>) => {
      return {
        ...state,
        isCreated: true,
        isError: false,
        data: [...state.data, action.payload],
      };
    },
    addPostFailure: (state, action: PayloadAction<string>) => {
      return {
        ...state,
        isCreated: false,
        isError: true,
        error: action.payload,
      };
    },
  },
});

export const { getPostsLoading, getPostsSuccess, getPostsFailure, addPostSuccess, addPostFailure } =
  posts.actions;
