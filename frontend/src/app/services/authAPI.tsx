import { api } from 'app/services';
import {
  LoginRequestType,
  LoginResponseType,
  RegisterRequestType,
  RegisterMailRequestType,
} from 'types';

export const authAPI = api.injectEndpoints({
  endpoints: (build) => ({
    register: build.mutation<void, RegisterMailRequestType>({
      query: ({ email, password, birthday, avatar }) => ({
        url: 'auth/register',
        method: 'POST',
        body: {
          email,
          password,
          birthday,
          avatar,
        },
      }),
    }),
    registerToken: build.mutation<void, 'token' & RegisterRequestType>({
      query: (token, ...registerData) => ({
        url: `auth/register/${token}`,
        method: 'POST',
        body: registerData,
      }),
    }),
    login: build.mutation<LoginResponseType, LoginRequestType>({
      query: ({ email, password }) => ({
        url: 'auth/login',
        method: 'POST',
        body: {
          email,
          password,
        },
      }),
    }),
    logout: build.mutation<void, void>({
      query: () => ({
        url: 'auth/logout',
        method: 'POST',
      }),
    }),
  }),
});

export const { useLoginMutation, useRegisterTokenMutation, useRegisterMutation } = authAPI;
