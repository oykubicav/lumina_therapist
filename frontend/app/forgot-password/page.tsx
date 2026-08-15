"use client";

import { useState } from "react";
import Link from "next/link";
import { postForgotPassword } from "@/lib/api";

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
      <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
        <div className="max-w-md text-center">
          <h2 className="text-xl font-medium mb-3">Kontrol et</h2>
          <p className="text-sm text-cbt-textSecondary mb-6">
            Eğer bu e-posta kayıtlıysa, birazdan bir reset linki alacaksın.
          </p>
          <Link href="/login" className="text-cbt-accent hover:underline">
            Giriş sayfasına dön
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-4">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-medium text-center mb-2">Şifremi unuttum</h1>
        <p className="text-sm text-cbt-textMuted text-center mb-8">
          E-posta adresini gir, sana bir reset linki gönderelim.
        </p>

        <form onSubmit={handleSubmit} className="bg-white dark:bg-cbt-dark-surface rounded-2xl p-6 shadow-soft space-y-4">
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 rounded-lg border border-cbt-border bg-transparent focus:outline-none focus:border-cbt-accent"
            placeholder="you@example.com"
          />
          <button
            type="submit"
            disabled={submitting}
            className="w-full py-3 rounded-xl bg-cbt-accent text-white font-medium disabled:opacity-50"
          >
            {submitting ? "Gönderiliyor..." : "Reset linki yolla"}
          </button>
          <p className="text-center text-xs">
            <Link href="/login" className="text-cbt-textMuted hover:text-cbt-accent">← Giriş sayfasına dön</Link>
          </p>
        </form>
      </div>
    </div>
  );
}