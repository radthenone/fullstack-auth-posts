// store.ts
import { configureStore } from '@reduxjs/toolkit';
import tagsReducer from './reducers';

const store = configureStore({
  reducer: {
    tags: tagsReducer,
  },
});

export default store;
