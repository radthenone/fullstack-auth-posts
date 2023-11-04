import { api } from 'app/services/api.tsx';
import { UserType } from 'types/userTypes';

export const authAPI = api.injectEndpoints({
  endpoints: (build) => ({
    login: build.mutation<UserType, { email: string; password: string }>({
      query: ({ email, password }) => ({
        url: 'auth/login',
        method: 'POST',
        body: { email, password },
      }),
    }),
  }),
});

export const { useLoginMutation } = authAPI;
