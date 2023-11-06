import { createApi, fetchBaseQuery, BaseQueryFn } from '@reduxjs/toolkit/query/react';
import { RootState } from 'app/store.tsx';
import { login, logout } from 'features/auth/services/authSlice.tsx';

const baseUrl = `${process.env.TEST_URL}`;

const baseQuery = fetchBaseQuery({
  baseUrl: baseUrl,
  credentials: 'include',
  prepareHeaders: (headers, { getState }) => {
    const token = (getState() as RootState).auth.token;
    if (token) {
      headers.set('authentication', `Bearer ${token}`);
    }
    return headers;
  },
});

const baseQueryWithRetry: BaseQueryFn = async (args, api, extraOptions) => {
  const result = await baseQuery(args, api, extraOptions);
  if (!result?.data || !result?.error) {
    return result;
  }

  if (result.error && result.error.status === 401) {
    const refreshToken = await baseQuery('/refresh', api, extraOptions);
    if (refreshToken.data) {
      const user = (api.getState() as RootState).auth.user;
      api.dispatch(login({ ...refreshToken.data, user }));
    } else {
      api.dispatch(logout());
    }
  }
  return result;
};

export const api = createApi({
  baseQuery: baseQueryWithRetry,

  tagTypes: ['Posts', 'Tags'],
  endpoints: () => ({}),
});
