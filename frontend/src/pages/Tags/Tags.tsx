import { useGetAllTagsQuery } from 'app/services/old';

const Tags = () => {
  const { data: tags, isError, isLoading, error } = useGetAllTagsQuery();

  if (isError) {
    return <p>{(error as Error).message}</p>;
  }

  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (tags === undefined) {
    return <p>No tags available.</p>;
  }

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
