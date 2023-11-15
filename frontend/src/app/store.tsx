import { configureStore, combineReducers } from '@reduxjs/toolkit';
import thunk from 'redux-thunk';
import logger from 'redux-logger';

import { api } from 'app/api';
import { posts } from 'app/posts/api';
import { tags } from 'app/tags/api';

const reducer = combineReducers({
  api: api.reducer,
  posts: posts.reducer,
  tags: tags.reducer,
});

const createMiddleware = () => {
  if (process.env.NODE_ENV === 'development') {
    return [thunk, logger];
  } else {
    return [thunk];
  }
};

const middleware = createMiddleware();

const store = configureStore({
  reducer: reducer,
  middleware: middleware,
  devTools: true,
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export default store;
