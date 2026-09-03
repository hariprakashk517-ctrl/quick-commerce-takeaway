export function getRemainingTime(expiryTime) {
  if (!expiryTime) {
    return {
      expired: true,
      hours: 0,
      minutes: 0,
      seconds: 0,
      totalSeconds: 0,
    };
  }

  const expiry = new Date(expiryTime).getTime();
  const now = Date.now();
  const difference = Math.max(0,Math.floor((expiry - now) / 1000));
  const hours = Math.floor(difference / 3600);
  const minutes = Math.floor((difference % 3600) / 60);
  const seconds = difference % 60;

  return {
    expired: difference === 0,
    totalSeconds: difference,
    hours,
    minutes,
    seconds,
  };
}