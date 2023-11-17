import { configureStore, combineReducers, ThunkDispatch, AnyAction } from '@reduxjs/toolkit';
import thunk from 'redux-thunk';
import logger from 'redux-logger';

import { api } from 'app/api';
import { posts } from 'app/posts/api';
import { tags, tag } from 'app/tags/api';
import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';

const reducer = combineReducers({
  api: api.reducer,
  posts: posts.reducer,
  tags: tags.reducer,
  tag: tag.reducer,
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

export type AppThunkDispatch = ThunkDispatch<RootState, any, AnyAction>;

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export const useAppDispatch = () => useDispatch<AppThunkDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
export default store;
