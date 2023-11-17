import { useGetTagQuery } from 'app/tags/hooks';

const PostDetail = () => {
  const { tag } = useGetTagQuery();

  if (!tag) {
    return <p>No tag available.</p>;
  }
  return (
    <>
      <p>{tag.name}</p>
    </>
  );
};

export default PostDetail;
