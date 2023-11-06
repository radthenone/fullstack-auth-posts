import { configureStore, combineReducers } from '@reduxjs/toolkit';
import thunk from 'redux-thunk';
import logger from 'redux-logger';

import { api } from 'app/services';
import { auth } from 'features/auth/services';

const rootReducer = combineReducers({
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

const store = configureStore({
  reducer: rootReducer,
  middleware: middleware,
  devTools: true,
});

export default store;

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
