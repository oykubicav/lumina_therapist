"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { postResendVerify } from "@/lib/api";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
        await register(email, password);
        setSuccessMessage(
  "Hesabın oluşturuldu. E-postana bir doğrulama linki gönderdik — kutunu kontrol et. " +
  "Linke tıkladıktan sonra giriş yapabilirsin."
);
    } catch (err: any) {
      setError(err?.message || "Kayıt başarısız oldu.");
    } finally {
      setSubmitting(false);
    }
  };
  if (successMessage) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
      <div className="max-w-md text-center">
        {/* Check ikonu */}
        <div className="w-16 h-16 rounded-full bg-emerald-100 dark:bg-emerald-900/20 flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>

        {/* Ana başlık */}
        <h2 className="text-xl font-medium text-cbt-text dark:text-cbt-dark-text mb-3">
          E-postana bir link gönderdik
        </h2>

        {/* Success mesajı — successMessage state'inden gelir */}
        <p className="text-sm text-cbt-textSecondary mb-4 leading-relaxed">
          {successMessage}
        </p>

        {/* YENİ — spam uyarısı */}
        <p className="text-xs text-cbt-textMuted mb-6">
          Email gelmediyse spam / gereksiz kutunu da kontrol et.
        </p>

        {/* Buton metni değişti */}
        <Link
          href="/login"
          className="inline-block px-6 py-3 rounded-xl bg-cbt-accent text-white font-medium"
        >
          E-postamı doğruladım — Giriş yap
        </Link>
      </div>
    </div>
  );
}

 

  return (
    <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-medium text-cbt-text dark:text-cbt-dark-text mb-2 text-center">
          Hesap oluştur
        </h1>
        <p className="text-sm text-cbt-textMuted text-center mb-8">
          İlerlemeni takip etmek ve geçmişini saklamak için
        </p>

        <form onSubmit={handleSubmit} className="bg-white dark:bg-cbt-dark-surface rounded-2xl p-6 shadow-soft space-y-4">
          <div>
            <label className="block text-xs text-cbt-textMuted mb-1">E-posta</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-cbt-border dark:border-cbt-dark-border bg-transparent text-cbt-text dark:text-cbt-dark-text focus:outline-none focus:border-cbt-accent"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="block text-xs text-cbt-textMuted mb-1">
              Şifre <span className="text-cbt-textMuted">(en az 8 karakter)</span>
            </label>
            <input
              type="password"
              required
              minLength={8}
              maxLength={128}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-cbt-border dark:border-cbt-dark-border bg-transparent text-cbt-text dark:text-cbt-dark-text focus:outline-none focus:border-cbt-accent"
            />
          </div>

          {error && (
            <p className="text-sm text-red-600">{error}</p>
          )}

          {}
          <div className="text-right">
            <button
              type="button" // Formun submit olmasını engellemek için type="button" çok önemlidir!
              onClick={async () => {
                await postResendVerify(email);
              }}
              className="text-xs text-cbt-accent hover:underline"
            >
              E-posta gelmediyse tekrar yolla
            </button>
          </div>
          {}

          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 rounded-xl bg-cbt-accent text-white font-medium disabled:opacity-50"
          >
            {submitting ? "Kayıt oluşturuluyor..." : "Hesap oluştur"}
          </button>

          <p className="text-xs text-cbt-textMuted leading-relaxed pt-2">
            Kayıt olurken KVKK ve kullanım politikalarımızı kabul etmiş olursun.
            İstediğin zaman hesabını silebilirsin.
          </p>

          <p className="text-center text-xs pt-2">
            <Link href="/login" className="text-cbt-accent hover:underline">
              Zaten hesabım var — Giriş yap
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}