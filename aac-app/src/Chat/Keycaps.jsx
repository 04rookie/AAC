import { Button } from "@mui/material";

export default function Keycaps({ name }) {
  return (
    <div>
      <Button variant="outlined">{name}</Button>
    </div>
  );
}
