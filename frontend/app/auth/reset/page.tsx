"use client";

import { useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { postResetPassword } from "@/lib/api";
import { Loader2, CheckCircle } from "lucide-react";

export default function ResetPasswordPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-cbt-bg dark:bg-cbt-dark-bg p-6">
          <Loader2 className="animate-spin text-cbt-textMuted" size={28} strokeWidth={1.8} />
        </div>
      }
    >
      <ResetPasswordContent />
    </Suspense>
  );
}

function ResetPasswordContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") || "";
  const [newPassword, setNewPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (newPassword !== confirm) {
      setError("Şifreler birbiriyle eşleşmiyor.");
      return;
    }
    if (!token) {
      setError("Bu bağlantı geçersiz. E-postandaki bağlantıyı kullandığından emin ol.");
      return;
    }

    setSubmitting(true);
    try {
      await postResetPassword(token, newPassword);
      setDone(true);
    } catch (err: any) {
      setError(err?.message || "Şifre güncellenemedi. Bağlantının süresi dolmuş olabilir.");
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
            <CheckCircle
              size={44}
              strokeWidth={1.5}
              className="mx-auto mb-6 text-cbt-success dark:text-cbt-dark-success"
            />
            <h2 className="text-[24px] font-semibold tracking-tight text-cbt-text dark:text-cbt-dark-text mb-3">
              Şifren güncellendi
            </h2>
            <p className="text-[14px] text-cbt-textSecondary dark:text-cbt-dark-textSecondary mb-8">
              Yeni şifrenle giriş yapabilirsin.
            </p>
            <Link
              href="/login"
              className="inline-flex items-center justify-center px-7 h-12 rounded-xl bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[15px] font-medium hover:opacity-85 transition-opacity"
            >
              Giriş yap
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
            Yeni şifre belirle
          </h1>
          <p className="text-[14px] text-cbt-textMuted dark:text-cbt-dark-textMuted text-center mb-10">
            Hesabın için yeni bir şifre oluştur
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-[13px] font-medium text-cbt-text dark:text-cbt-dark-text mb-1.5">
                Yeni şifre
              </label>
              <input
                type="password"
                required
                minLength={8}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full px-4 h-12 rounded-xl border border-cbt-border dark:border-cbt-dark-border bg-cbt-surface dark:bg-cbt-dark-surface text-[15px] text-cbt-text dark:text-cbt-dark-text focus:outline-none focus:border-cbt-borderStrong dark:focus:border-cbt-dark-borderStrong transition-colors"
              />
              <p className="mt-1.5 text-[12px] text-cbt-textMuted dark:text-cbt-dark-textMuted">
                En az 8 karakter
              </p>
            </div>

            <div>
              <label className="block text-[13px] font-medium text-cbt-text dark:text-cbt-dark-text mb-1.5">
                Yeni şifre (tekrar)
              </label>
              <input
                type="password"
                required
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                className="w-full px-4 h-12 rounded-xl border border-cbt-border dark:border-cbt-dark-border bg-cbt-surface dark:bg-cbt-dark-surface text-[15px] text-cbt-text dark:text-cbt-dark-text focus:outline-none focus:border-cbt-borderStrong dark:focus:border-cbt-dark-borderStrong transition-colors"
              />
            </div>

            {error && (
              <p className="text-[13px] text-cbt-danger dark:text-cbt-dark-danger leading-relaxed">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full h-12 rounded-xl bg-cbt-text dark:bg-cbt-dark-text text-cbt-bg dark:text-cbt-dark-bg text-[15px] font-medium hover:opacity-85 transition-opacity disabled:opacity-40"
            >
              {submitting ? "Kaydediliyor…" : "Şifreyi kaydet"}
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}
