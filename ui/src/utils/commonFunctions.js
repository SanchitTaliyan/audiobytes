import { formatDistanceToNow, isToday, isYesterday } from "date-fns";

export const parseFloatToFixed = (value) => {
  const formattedValue = parseFloat(value).toFixed(1);
  return formattedValue.endsWith(".0")
    ? formattedValue.slice(0, -2)
    : formattedValue;
};

export const getRelativeDate = (date) => {
  if (isToday(date)) {
    return "Today";
  }
  if (isYesterday(date)) {
    return "Yesterday";
  }
  const distance = formatDistanceToNow(date, { addSuffix: true });
  return distance;
};
