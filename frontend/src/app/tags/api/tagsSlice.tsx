import { createSlice } from '@reduxjs/toolkit';
import { tagsStateType, TagType } from 'types';
import { tagsState } from 'app/tags/state';
import { tagThunk } from 'app/tags/thunk';

const initialTagsState: tagsStateType = tagsState;

export const tags = createSlice({
  name: 'tags',
  initialState: initialTagsState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(tagThunk.getTags.pending, (state) => {
        state.isLoading = true;
        state.isSuccess = false;
        state.isError = false;
        state.data = [];
      })
      .addCase(tagThunk.getTags.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.isError = false;
        state.data = action.payload;
      })
      .addCase(tagThunk.getTags.rejected, (state, action) => {
        state.isLoading = false;
        state.isSuccess = false;
        state.isError = true;
        state.error = action.payload as string;
      })
      .addCase(tagThunk.addTag.fulfilled, (state, action) => {
        state.isCreated = true;
        state.isError = false;
        state.data.push(action.payload as TagType);
      })
      .addCase(tagThunk.addTag.rejected, (state, action) => {
        state.isLoading = false;
        state.isCreated = false;
        state.isError = true;
        state.error = action.payload as string;
      });
  },
});
