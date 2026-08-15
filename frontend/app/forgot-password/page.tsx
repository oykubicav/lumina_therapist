"use client";

import { useState } from "react";
import Link from "next/link";
import { postForgotPassword } from "@/lib/api";
import { MailCheck } from "lucide-react";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await postForgotPassword(email);
      setDone(true);
    } finally {
      setSubmitting(false);
    }
  };

  if (done) {
    return (
      <div className="min-h-screen flex flex-col bg-cbt-bg dark:bg-cbt-dark-bg">
        <header className="px-6 py-5">
          <Link
            href="/"
            className="text-[17px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text"
          >
            Neva
          </Link>
        </header>
        <main className="flex-1 flex items-center justify-center px-6 pb-24">
          <div className="max-w-sm text-center">
            <MailCheck
              size={44}
              strokeWidth={1.5}
              className="mx-auto mb-6 text-cbt-success dark:text-cbt-dark-success"
            />
            <h2 className="text-[24px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text mb-3">
              E-postanı kontrol et
            </h2>
            <p className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary leading-relaxed mb-8">
              Bu adres kayıtlıysa, şifreni yenilemen için bir bağlantı
              gönderdik. Birkaç dakika içinde gelmezse spam klasörüne bak.
            </p>
            <Link
              href="/login"
              className="text-[14px] font-medium text-cbt-text dark:text-cbt-dark-text hover:underline underline-offset-2"
            >
              Girişe dön
            </Link>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-cbt-bg dark:bg-cbt-dark-bg">
      <header className="px-6 py-5">
        <Link
          href="/"
          className="text-[17px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text"
        >
          Neva
        </Link>
      </header>

      <main className="flex-1 flex items-center justify-center px-6 pb-24">
        <div className="w-full max-w-sm">
          <h1 className="text-[28px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text mb-2 text-center">
            Şifreni yenile
          </h1>
          <p className="text-[14px] text-cbt-textMuted dark:text-cbt-dark-textMuted text-center mb-10">
            E-posta adresini yaz, sana bir yenileme bağlantısı gönderelim
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-[13px] font-medium text-cbt-text dark:text-cbt-dark-text mb-1.5">
                E-posta
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 h-12 rounded-xl border border-cbt-border dark:border-cbt-dark-border bg-cbt-surface dark:bg-cbt-dark-surface text-[15px] text-cbt-text dark:text-cbt-dark-text placeholder:text-cbt-textMuted focus:outline-none focus:border-cbt-borderStrong dark:focus:border-cbt-dark-borderStrong transition-colors"
                placeholder="ornek@eposta.com"
              />
            </div>
            <button
              type="submit"
              disabled={submitting}
              className="w-full h-12 rounded-xl bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[15px] font-medium hover:opacity-85 transition-opacity disabled:opacity-40"
            >
              {submitting ? "Gönderiliyor…" : "Bağlantı gönder"}
            </button>
          </form>

          <p className="mt-8 text-center text-[13px]">
            <Link
              href="/login"
              className="text-cbt-textMuted dark:text-cbt-dark-textMuted hover:text-cbt-text dark:hover:text-cbt-dark-text transition-colors"
            >
              Girişe dön
            </Link>
          </p>
        </div>
      </main>
    </div>
  );
}
