const MaxTextCard = (props: { text: string }) => {
  const MAX_LENGTH = 100;
  return (
    <>
      {props.text.length > MAX_LENGTH ? (
        <>{`${props.text.substring(0, MAX_LENGTH)}...`}</>
      ) : (
        <>{props.text}</>
      )}
    </>
  );
};

export default MaxTextCard;
