/// <reference types="vite/client" />
type ImportMetaEnv = {
  readonly API_BACKEND_URL: string;
  readonly NODE_ENV: string;
  // more env variables...
};

type ImportMeta = {
  readonly env: ImportMetaEnv;
};
