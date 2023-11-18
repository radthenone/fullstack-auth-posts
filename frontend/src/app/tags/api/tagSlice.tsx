import { createSlice } from '@reduxjs/toolkit';
import { tagStateType } from 'types';
import { tagState } from 'app/tags/state';
import { tagThunk } from 'app/tags/thunk';

const initialTagState: tagStateType = tagState;

export const tag = createSlice({
  name: 'tag',
  initialState: initialTagState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(tagThunk.getTag.pending, (state) => {
        state.isLoading = true;
        state.isSuccess = false;
        state.isError = false;
      })
      .addCase(tagThunk.getTag.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isSuccess = true;
        state.isError = false;
        state.data = action.payload;
      })
      .addCase(tagThunk.getTag.rejected, (state, action) => {
        state.isLoading = false;
        state.isSuccess = false;
        state.isError = true;
        state.error = action.payload as string;
      })
      .addCase(tagThunk.modifyTag.fulfilled, (state, action) => {
        state.isUpdated = true;
        state.isError = false;
        state.data = action.payload;
      })
      .addCase(tagThunk.modifyTag.rejected, (state, action) => {
        state.isUpdated = false;
        state.isError = true;
        state.error = action.payload as string;
      })
      .addCase(tagThunk.removeTag.fulfilled, (state) => {
        state.isDeleted = true;
        state.isError = false;
        state.data = null;
      })
      .addCase(tagThunk.removeTag.rejected, (state, action) => {
        state.isDeleted = false;
        state.isError = true;
        state.error = action.payload as string;
      });
  },
});
