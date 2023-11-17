import { createAsyncThunk } from '@reduxjs/toolkit';
import { TagType } from 'types';
import { tagAPI } from 'app/tags/services';

const tagThunk = {
  getTags: createAsyncThunk('tags/getTags', async (): Promise<TagType[]> => {
    return await tagAPI.getTags();
  }),
  getTag: createAsyncThunk('tags/getTag', async (id: number): Promise<TagType> => {
    return await tagAPI.getTag(id);
  }),
  addTag: createAsyncThunk(
    'tags/addTag',
    async (tag: { name: string } | ''): Promise<TagType | void> => {
      return await tagAPI.createTag(tag);
    },
  ),
  modifyTag: createAsyncThunk('tags/modifyTag', async (tag: TagType): Promise<TagType> => {
    return await tagAPI.updateTag(tag);
  }),
  removeTag: createAsyncThunk('tags/removeTag', async (id: number): Promise<void> => {
    return await tagAPI.deleteTag(id);
  }),
};

export { tagThunk };
