import { cookies } from "next/headers";

export async function getLocale(): Promise<"en" | "fr" | "ar"> {
  const cookieStore = await cookies();

  const locale =
    cookieStore.get("locale")?.value ||
    cookieStore.get("language")?.value ||
    "en";

  if (locale === "fr" || locale === "ar") {
    return locale;
  }

  return "en";
}
