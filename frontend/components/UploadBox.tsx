type Props = {
  file: File | null;
  onFileChange: (file: File | null) => void;
  language?: string;
};

const labels: any = {
  en: {
    title: "Upload your contract",
    subtitle: "PDF or DOCX, max 10MB",
    selected: "Selected:",
  },
  fr: {
    title: "Télécharger votre contrat",
    subtitle: "PDF ou DOCX, max 10MB",
    selected: "Fichier sélectionné :",
  },
  ar: {
    title: "ارفع عقدك",
    subtitle: "PDF أو DOCX، الحد الأقصى 10MB",
    selected: "تم اختيار:",
  },
};

export default function UploadBox({
  file,
  onFileChange,
  language = "en",
}: Props) {
  const t = labels[language] || labels.en;

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
        {t.title}
      </h3>

      <p className="mt-2 text-sm text-gray-500">
        {t.subtitle}
      </p>

      {file && (
        <p className="mt-4 text-sm font-medium text-green-700">
          {t.selected} {file.name}
        </p>
      )}
    </label>
  );
}