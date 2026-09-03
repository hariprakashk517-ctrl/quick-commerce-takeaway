import { useEffect, useState } from "react";
import { getRemainingTime } from "../../utils/countdown";

function CountdownTimer({ expiryTime }) {
  const [time, setTime] = useState(
    getRemainingTime(expiryTime)
  );

  useEffect(() => {
    setTime(getRemainingTime(expiryTime));

    const interval = setInterval(() => {
      const remaining =
        getRemainingTime(expiryTime);

      setTime(remaining);

      if (remaining.expired) {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [expiryTime]);

  if (time.expired) {
    return (
      <span>
        Expired
      </span>
    );
  }

  const pad = (value) =>
    String(value).padStart(2, "0");

  return (
    <span>
      {pad(time.hours)}:
      {pad(time.minutes)}:
      {pad(time.seconds)}
    </span>
  );
}

export default CountdownTimer;