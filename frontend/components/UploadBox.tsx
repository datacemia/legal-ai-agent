type Props = {
  file: File | null;
  onFileChange: (file: File | null) => void;
  language?: string;
};

const labels: any = {
  en: {
    title: "Upload your contract",
    subtitle: "PDF, DOCX & scanned documents",
    secure: "Secure upload",
    ocr: "OCR supported",
    browse: "Drag & drop or click to browse",
    selected: "Selected:",
  },

  fr: {
    title: "Importez votre contrat",
    subtitle: "PDF, DOCX et documents scannés",
    secure: "Import sécurisé",
    ocr: "OCR pris en charge",
    browse: "Glissez-déposez ou cliquez pour parcourir",
    selected: "Fichier sélectionné :",
  },

  ar: {
    title: "ارفع عقدك",
    subtitle: "ملفات PDF و DOCX والمستندات الممسوحة ضوئياً",
    secure: "رفع آمن",
    ocr: "يدعم OCR",
    browse: "اسحب الملف هنا أو اضغط للاختيار",
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
    <div className="space-y-4">
      <label className="group relative block cursor-pointer overflow-hidden rounded-[32px] border border-slate-200 bg-gradient-to-br from-white via-slate-50 to-blue-50/40 p-10 transition-all duration-300 hover:border-blue-200 hover:shadow-xl">

        <div className="absolute inset-0 rounded-[32px] border-2 border-dashed border-slate-200 transition-all duration-300 group-hover:border-blue-300" />

        <input
          type="file"
          accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          className="hidden"
          onChange={(e) => onFileChange(e.target.files?.[0] || null)}
        />

        <div className="relative z-10 flex flex-col items-center justify-center text-center">

          <div className="flex h-20 w-20 items-center justify-center rounded-3xl bg-white shadow-sm ring-1 ring-slate-200">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="h-10 w-10 text-blue-600"
            >
              <path d="M14 3.75H7A2.25 2.25 0 0 0 4.75 6v12A2.25 2.25 0 0 0 7 20.25h10A2.25 2.25 0 0 0 19.25 18V9l-5.25-5.25Z" />
              <path d="M14 3.75V9h5.25" />
              <path d="M12 17.25V11.5" />
              <path d="m8.5 11.5 3.5-3.5 3.5 3.5" />
            </svg>
          </div>

          <h3 className="mt-6 text-2xl font-semibold tracking-tight text-slate-900">
            {t.title}
          </h3>

          <p className="mt-3 text-base text-slate-500">
            {t.subtitle}
          </p>

          <div className="mt-5 flex flex-wrap items-center justify-center gap-3">

            <span className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="h-4 w-4 text-blue-600"
              >
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z" />
              </svg>

              {t.secure}
            </span>

            <span className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="h-4 w-4 text-blue-600"
              >
                <path d="m12 3-1.9 3.9L6 9l4.1 2.1L12 15l1.9-3.9L18 9l-4.1-2.1L12 3Z" />
                <path d="M5 19l.75-1.5L7.25 17 5.75 16.25 5 14.75l-.75 1.5L2.75 17l1.5.75L5 19Z" />
              </svg>

              {t.ocr}
            </span>

          </div>

          <div className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-slate-500">

            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              className="h-4 w-4 text-blue-600"
            >
              <path d="M12 16V8" />
              <path d="m8.5 11.5 3.5-3.5 3.5 3.5" />
              <path d="M20 16.5A3.5 3.5 0 0 0 16.5 13H15a5 5 0 1 0-9.6 1.5A3 3 0 0 0 6 20h11a3 3 0 0 0 3-3.5Z" />
            </svg>

            <span>{t.browse}</span>

          </div>

        </div>
      </label>

      {file && (
        <div className="flex items-center justify-between rounded-2xl border border-green-200 bg-green-50/70 px-5 py-4 shadow-sm">

          <div className="flex items-center gap-4">

            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-green-600 text-white">
              ✓
            </div>

            <div className="flex flex-col">

              <span className="text-sm font-semibold text-slate-900">
                {t.selected} {file.name}
              </span>

              <span className="text-xs text-slate-500">
                {(file.size / (1024 * 1024)).toFixed(2)} MB
              </span>

            </div>

          </div>

          <button
            type="button"
            onClick={() => onFileChange(null)}
            className="rounded-full p-2 text-slate-400 transition hover:bg-white hover:text-red-500"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              className="h-5 w-5"
            >
              <path d="M18 6 6 18" />
              <path d="m6 6 12 12" />
            </svg>
          </button>

        </div>
      )}
    </div>
  );
}
