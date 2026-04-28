type Props = {
  file: File | null;
  onFileChange: (file: File | null) => void;
};

export default function UploadBox({ file, onFileChange }: Props) {
  return (
    <label className="block cursor-pointer rounded-2xl border-2 border-dashed border-gray-300 bg-white p-10 text-center hover:border-black transition">
      <input
        type="file"
        accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        className="hidden"
        onChange={(e) => onFileChange(e.target.files?.[0] || null)}
      />

      <div className="text-4xl mb-3">📄</div>

      <h3 className="text-lg font-semibold text-gray-900">
        Upload your contract
      </h3>

      <p className="mt-2 text-sm text-gray-500">
        PDF or DOCX, max 10MB
      </p>

      {file && (
        <p className="mt-4 text-sm font-medium text-green-700">
          Selected: {file.name}
        </p>
      )}
    </label>
  );
}