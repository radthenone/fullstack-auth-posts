import { useModifyTagMutation, useGetTagQuery } from 'app/tags/hooks';
import { Button, FormLabel, TextField } from '@mui/material';
import { FormEvent, useEffect, useState } from 'react';
import { TagType } from 'types';

export const UpdateTagForm = () => {
  const { setModifyTag, isError, isUpdated, error } = useModifyTagMutation();
  const { tag: oldTag } = useGetTagQuery();
  const [name, setName] = useState<string>(oldTag?.name ?? '');

  useEffect(() => {
    setName(oldTag?.name ?? '');
  }, [oldTag]);

  const tag: TagType = {
    id: Number(oldTag?.id),
    name: name,
  };

  const handleModifyTag = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setModifyTag(tag);
  };

  return (
    <>
      <form onSubmit={handleModifyTag}>
        <FormLabel htmlFor="name">Post name</FormLabel>
        {isError && name === '' ? <p>Enter tag name</p> : <p>{name}</p>}
        {isError && <p>{error}</p>}
        <TextField
          id="name"
          name={oldTag?.name}
          type="name"
          placeholder="Enter tag name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Button type="submit">Change Tag</Button>
      </form>
      {isUpdated && <h1>Updated</h1>}
      {JSON.stringify(tag)}
    </>
  );
};
