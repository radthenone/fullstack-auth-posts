export const createUniqueIdsToEnd = (data: Array<any>) => {
  const maxId = Math.max(...data);
  return maxId >= 0 ? maxId + 1 : 1;
};
