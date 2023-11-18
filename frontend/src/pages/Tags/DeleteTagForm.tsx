import { useDeleteTagMutation, useGetTagQuery } from 'app/tags/hooks';
import { Button } from '@mui/material';
import { FormEvent } from 'react';
import { Link } from 'react-router-dom';

export const DeleteTagForm = () => {
  const { setDeleteTag, isError, isDeleted, error } = useDeleteTagMutation();
  const { tag } = useGetTagQuery();
  const handleDeleteTag = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (tag !== null && Number(tag.id) !== 0) {
      setDeleteTag({ id: Number(tag.id) });
    }
  };

  if (isDeleted) {
    return (
      <>
        <h1>Tag deleted</h1>
        <Button variant="contained" component={Link} to="/tags">
          Go back
        </Button>
      </>
    );
  }
  if (isError) {
    return <p>{error}</p>;
  }

  return (
    <>
      <form onSubmit={handleDeleteTag}>
        <Button variant="contained" type="submit">
          Delete Tag
        </Button>
      </form>
    </>
  );
};
