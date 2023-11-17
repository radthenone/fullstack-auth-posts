import { useGetTagsQuery } from 'app/tags/hooks';

const Tags = () => {
  const { data: tags, isError, isLoading, error } = useGetTagsQuery();

  if (isError) {
    return <p>{error}</p>;
  }

  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (!tags) {
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
