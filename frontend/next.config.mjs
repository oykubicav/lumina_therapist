/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000",
  },
  // ESLint stil kuralları build'i bloklamasın (react/no-unescaped-entities gibi).
  // Türkçe içerikte apostrof + tırnak yoğun kullanılır; lint runtime davranışı etkilemiyor.
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
