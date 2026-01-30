import clsx from "clsx";

export default function Card({ children, className, hoverable = true }) {
  return (
    <div
      className={clsx(
        "bg-dark-800 rounded-lg p-6 border border-dark-700",
        hoverable &&
          "hover:border-primary-600 hover:shadow-lg hover:shadow-primary-900/20",
        "transition-all",
        className,
      )}
    >
      {children}
    </div>
  );
}
