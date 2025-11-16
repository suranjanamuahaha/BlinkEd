export default function SignInPopup({ onClose, onSignIn }) {
  return (
    <div className="fixed inset-0 bg-black/75 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-80 text-center">
        <h2 className="text-xl font-semibold mb-3">Please Sign In</h2>
        <p className="text-gray-600 mb-5">
          You’ve reached the free limit. Sign in to continue using BlinkEd.
        </p>

        <button
          onClick={onSignIn}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 mb-3"
        >
          Sign In
        </button>

        <button
          onClick={onClose}
          className="w-full bg-gray-200 py-2 rounded hover:bg-gray-300"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}
