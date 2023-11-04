import { useState, useEffect } from 'react';
import { ApiProvider } from '@reduxjs/toolkit/dist/query/react';
import { TagsData } from 'types/data.tsx';
import { useGetTagsQuery } from 'app/services/tagsAPI.tsx';

const Tags = () => {
  const { data, isError, isLoading, error }: TagsData[] = useGetTagsQuery();

  if (isError) {
    return <p>{error.message}</p>;
  }

  if (isLoading) {
    return <p>Loading...</p>;
  }

  const tags = data.results;

  return (
    <>
      {tags.map((tag) => (
        <div key={tag.id}>
          <p>{tag.name}</p>
        </div>
      ))}
    </>
  );
};

export default Tags;
