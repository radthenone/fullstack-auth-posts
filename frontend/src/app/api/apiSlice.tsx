import { createSlice } from '@reduxjs/toolkit';
import { apiState } from 'app/api/apiState';

const initialState = apiState;

export const api = createSlice({
  name: 'api',
  initialState,
  reducers: {},
});
