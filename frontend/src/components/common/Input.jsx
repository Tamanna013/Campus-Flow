import clsx from "clsx";

export default function Input({ label, error, className, ...props }) {
  return (
    <div>
      {label && (
        <label className="block text-sm font-medium text-gray-300 mb-2">
          {label}
        </label>
      )}

      <input
        {...props}
        className={clsx(
          "w-full px-4 py-2 rounded-lg",
          "bg-white text-black placeholder-gray-500",
          "border border-gray-300",
          "focus:outline-none focus:ring-2 focus:ring-primary-500",
          error && "border-red-500",
          className,
        )}
      />

      {error && <p className="mt-1 text-sm text-red-400">{error}</p>}
    </div>
  );
}
