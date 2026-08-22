import type { Metadata } from "next";
import StudyAgentDemoClient from "./StudyAgentDemoClient";

export const metadata: Metadata = {
  title: "عرض Runexa Study Agent | Runexa Systems",
  description:
    "شاهد Runexa Study Agent وهو يحول المواد الدراسية إلى ملخصات واختبارات وبطاقات مراجعة وخرائط تعلم وخطط مراجعة مخصصة بالذكاء الاصطناعي.",

  alternates: {
    canonical: "https://runexa.ai/ar/demo/study-agent",
    languages: {
      en: "https://runexa.ai/en/demo/study-agent",
      fr: "https://runexa.ai/fr/demo/study-agent",
      ar: "https://runexa.ai/ar/demo/study-agent",
      "x-default": "https://runexa.ai/demo/study-agent",
    },
  },

  openGraph: {
    title: "عرض Runexa Study Agent",
    description:
      "شاهد كيف يحول Runexa Study المواد الدراسية إلى مساحة تعلم متكاملة مدعومة بالذكاء الاصطناعي.",
    url: "https://runexa.ai/ar/demo/study-agent",
    siteName: "Runexa Systems",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "عرض Runexa Study Agent",
      },
    ],
    locale: "ar_AR",
    type: "website",
  },

  twitter: {
    card: "summary_large_image",
    title: "عرض Runexa Study Agent",
    description:
      "ملخصات، اختبارات، بطاقات مراجعة، خرائط تعلم وخطط مراجعة مخصصة بالذكاء الاصطناعي.",
    images: ["/og-image.png"],
  },

  robots: {
    index: true,
    follow: true,
  },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Runexa Study Agent",
  applicationCategory: "EducationalApplication",
  operatingSystem: "Web",
  url: "https://runexa.ai/ar/demo/study-agent",
  inLanguage: "ar",
  description:
    "مساعد دراسي بالذكاء الاصطناعي لإنشاء الملخصات والاختبارات وبطاقات المراجعة وخرائط التعلم والصوت وخطط المراجعة المخصصة.",
};

export default function StudyAgentDemoArabicPage() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLd),
        }}
      />

      <StudyAgentDemoClient />
    </>
  );
}