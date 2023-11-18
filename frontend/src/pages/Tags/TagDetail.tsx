import { useGetTagQuery } from 'app/tags/hooks';
import { UpdateTagForm } from 'pages/Tags/UpdateTagForm.tsx';
import { DeleteTagForm } from 'pages/Tags/DeleteTagForm.tsx';

const PostDetail = () => {
  const { tag } = useGetTagQuery();

  if (!tag) {
    return <p>No tag available.</p>;
  }
  return (
    <>
      <p>{tag.name}</p>
      <UpdateTagForm />
      <DeleteTagForm />
    </>
  );
};

export default PostDetail;
