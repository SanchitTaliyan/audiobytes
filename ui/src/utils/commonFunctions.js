export const parseFloatToFixed = (value) => {
  const formattedValue = parseFloat(value).toFixed(1);
  return formattedValue.endsWith('.0') ? formattedValue.slice(0, -2) : formattedValue;
};
