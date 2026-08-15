"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { postResendVerify } from "@/lib/api";


export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [needsVerify, setNeedsVerify] = useState(false);
  const [resendMessage, setResendMessage] = useState("");


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(email, password);
      router.push("/");
} catch (err: any) {
  // 403 → email verify eksik
  if (err?.status === 403 || err?.message?.includes("doğrula")) {
    setError("E-posta adresini henüz doğrulamadın. Kayıt sırasında gelen linke tıkla — spam kutunu da kontrol et.");
    setNeedsVerify(true);
  } else {
    setError(err?.message || "Giriş başarısız oldu.");
  }
} finally {
  setSubmitting(false);
}}
    

  return (
    <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-medium text-cbt-text dark:text-cbt-dark-text mb-2 text-center">
          Giriş yap
        </h1>
        <p className="text-sm text-cbt-textMuted text-center mb-8">
          Hesabına giriş yaparak sohbete devam et
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
            <label className="block text-xs text-cbt-textMuted mb-1">Şifre</label>
            <input
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-cbt-border dark:border-cbt-dark-border bg-transparent text-cbt-text dark:text-cbt-dark-text focus:outline-none focus:border-cbt-accent"
            />
          </div>

          {error && (
            <p className="text-sm text-red-600">{error}</p>
          )}
          {needsVerify && (
  <button
    type="button"
    onClick={async () => {
      await postResendVerify(email);
      setResendMessage("Doğrulama linki tekrar gönderildi. E-postanı kontrol et.");
      setNeedsVerify(false);
    }}
    className="text-sm text-cbt-accent hover:underline mt-2"
  >
    Doğrulama linkini tekrar yolla
  </button>
)}
{resendMessage && (
  <p className="text-sm text-emerald-600 mt-2">{resendMessage}</p>
)}


          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 rounded-xl bg-cbt-accent text-white font-medium disabled:opacity-50"
          >
            {submitting ? "Giriş yapılıyor..." : "Giriş yap"}
          </button>

          <div className="flex justify-between text-xs pt-2">
            <Link href="/forgot-password" className="text-cbt-textMuted hover:text-cbt-accent">
              Şifremi unuttum
            </Link>
            <Link href="/register" className="text-cbt-accent hover:underline">
              Hesap oluştur
            </Link>
          </div>
        </form>

        <p className="text-center text-xs text-cbt-textMuted mt-6">
          <Link href="/" className="hover:text-cbt-accent">Anonim olarak devam et</Link>
        </p>
      </div>
    </div>
  );
}