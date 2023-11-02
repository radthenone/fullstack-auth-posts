import { createAction, createReducer } from '@reduxjs/toolkit';
import { TagsData } from 'types/data.tsx';
export const setTags = createAction<TagsData[]>('tags/setTags');
const initialState: TagsData[] = [];

const tagsReducer = createReducer(initialState, (builder) => {
  builder.addCase(setTags, (_state, action) => {
    return action.payload;
  });
});

export default tagsReducer;
