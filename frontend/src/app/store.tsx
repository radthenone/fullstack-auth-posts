import { configureStore, combineReducers } from '@reduxjs/toolkit';
import thunk from 'redux-thunk';
import logger from 'redux-logger';

import { api } from 'app/services/old';
import { auth } from 'features/auth/services';

const reducer = combineReducers({
  api: api.reducer,
  auth: auth.reducer,
});

const createMiddleware = () => {
  if (process.env.NODE_ENV === 'development') {
    return [thunk, logger, api.middleware];
  } else {
    return [api.middleware];
  }
};

const middleware = createMiddleware();

export const store = configureStore({
  reducer: reducer,
  middleware: middleware,
  devTools: true,
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
